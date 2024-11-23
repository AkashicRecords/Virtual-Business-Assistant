# Dependency Management

## Overview
Dependencies are strictly versioned and managed through pip-tools.

## Files
- `requirements.in`: Core dependencies with version constraints
- `requirements-dev.in`: Development dependencies
- `requirements.txt`: Locked production dependencies
- `requirements-dev.txt`: Locked development dependencies

## Updating Dependencies
1. Update version constraints in `.in` files
2. Generate new requirements:
   ```bash
   pip-compile requirements.in
   pip-compile requirements-dev.in
   ```
3. Test with new versions:
   ```bash
   pip-sync requirements-dev.txt
   pytest
   ```
4. Commit both `.in` and `.txt` files

## Rolling Back
1. Git checkout previous requirements files
2. Sync environment:
   ```bash
   pip-sync requirements-dev.txt
   ```

## Adding New Dependencies
1. Add to appropriate `.in` file
2. Regenerate requirements
3. Test thoroughly
4. Commit all changes 