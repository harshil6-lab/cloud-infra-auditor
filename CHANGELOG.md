# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - 2026-07-08

### Added
- Parallel multi-region AWS scanning.
- Shared `auditor/utils/parallel.py` utility built on `ThreadPoolExecutor` for concurrent scan execution.
- Rich CLI progress bar shown during scans.
- Rich scan summary panel (`auditor/ui/summary.py`) displayed after each scan.

### Changed
- CLI output made more consistent across `scan`, `report`, and `cleanup` commands.
- Scan commands now use the shared parallel scanning utility instead of running region scans sequentially.

### Performance
- Typical multi-region scan time reduced from ~60–65 seconds to ~8–10 seconds.

### Refactored
- Consolidated duplicated per-scanner concurrency logic into a single shared utility.
- Clearer separation of concerns between scanning, UI, and reporting layers.

### Testing
- Existing Pytest + Moto test suite verified against the refactored scanning and concurrency logic.

### Documentation
- README updated to reflect parallel scanning, new UI layer, and current architecture.
- Added "What's New in v1.1.0" section to README.
- Added CLI preview placeholders for scan and cleanup commands.