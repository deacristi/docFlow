# Changelog

All notable changes to docFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2025-12-06

### Added
- **Kiro IDE Steering Rules** - Automatic enforcement via `.kiro/steering/` files
  - `context-monitoring.md` - AI context health monitoring
  - `phase-gates.md` - Phase gate enforcement
- **Checkpoint System** - Git-based progress saving with `scripts/checkpoint.py`
- **Living Code Freshness Checker** - `scripts/check_freshness.py` for documentation staleness detection
- **Recovery Protocols** - `templates/recovery_protocols.md` for failure recovery
- **Phase Gate Checklist** - `templates/phase_gate_checklist.md` for gate verification

### Changed
- Updated all documentation to v3.1
- Improved workflow guide with clearer gate phrases
- Enhanced development standards with more examples

### Fixed
- Windows compatibility for all scripts (PowerShell support)

## [3.0.0] - 2025-11-01

### Added
- 6-phase workflow with mandatory gate checks
- Living Code Context pattern
- Development standards with automated enforcement
- Template system for documentation

### Changed
- Complete restructure of documentation
- New philosophy: "Production-grade without over-engineering"

## [2.0.0] - 2025-09-01

### Added
- Initial public release
- Basic workflow documentation
- Template files

---

## Upgrade Guide

### From v3.0 to v3.1

1. Copy new steering rules to `.kiro/steering/`
2. Add checkpoint script to `scripts/`
3. Add freshness checker to `scripts/`
4. Update `.gitignore` to include `.docflow_checkpoints/`

### From v2.0 to v3.0

1. Review new 6-phase workflow
2. Update templates to new format
3. Implement Living Code Context structure
4. Add development standards enforcement
