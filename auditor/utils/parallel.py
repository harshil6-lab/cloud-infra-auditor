from auditor.aws.regions import get_regions
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)


def scan_scanners(
    scan_function,
    profile_name=None,
    max_workers=None,
    task_description="AWS Resource Scanning",
    progress_bar=True,
):
    findings = []
    regions = get_regions(profile_name)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(task_description, total=len(regions))
        with ThreadPoolExecutor(max_workers=min(8, len(regions))) as executor:
            future_to_region = {}

            for region in regions:
                future = executor.submit(scan_function, region)
                future_to_region[future] = region

            for future in as_completed(future_to_region):
                region = future_to_region[future]
                try:
                    region_findings = future.result()
                    progress.update(task, advance=1)
                    findings.extend(region_findings)
                except Exception as e:
                    progress.update(task, advance=1)
                    print(f"[red]Error scanning region {region}: {e}[/red]")

    return {"regions_scanned": len(regions), "findings": findings}
