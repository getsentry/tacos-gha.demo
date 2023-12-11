# tacos-demo

## Description

<https://www.notion.so/sentry/TACOS-Sync-8d61ee6576a24d49acd43ad796760a11?pvs=4#a505c2afaf7a46118428bb0e32568ae4>

## Developer Setup

To install required tools, please run:

```
brew bundle
tfenv install
tgenv install
```

(You may need to [install homebrew].)

## Onboarding

Each developer has to submit a simple change:

```
make terraform/env.$USER
git commit -am "feat: onboarding dev $USER"
```

## Usage

To do the common plan / review / apply cycle:

```
sudo-sac terragrunt run-all plan -out plan
sudo-sac terragrunt run-all apply plan
```

[install homebrew]: https://brew.sh/
