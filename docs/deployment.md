# Deployment Process

## Version Management

Versions follow semantic versioning (MAJOR.MINOR.PATCH).

### Creating a New Release
1. Go to Actions tab in GitHub
2. Select "Version Management" workflow
3. Click "Run workflow"
4. Choose version increment type:
   - patch: Bug fixes
   - minor: New features
   - major: Breaking changes

This will:
1. Bump version numbers
2. Create a git tag
3. Trigger deployment workflow

## Deployment Process

The deployment workflow:
1. Runs all tests
2. Builds executables for all platforms
3. Creates GitHub release
4. Uploads artifacts

## Artifacts

Each release includes:
- Windows installer (.exe)
- macOS disk image (.dmg)
- Source distribution (.tar.gz)

## Environments

### Development
- Branch: develop
- Auto-deploys: No
- Requirements: All dev dependencies

### Staging
- Branch: staging
- Auto-deploys: On PR merge
- Requirements: Production dependencies

### Production
- Branch: main
- Auto-deploys: On version tag
- Requirements: Production dependencies 