# tacos-demo

## Description

<https://www.notion.so/sentry/TACOS-Sync-8d61ee6576a24d49acd43ad796760a11?pvs=4#a505c2afaf7a46118428bb0e32568ae4>

## Developer Setup

To install required tools, please run: (after you [install homebrew])

```
brew bundle
tfenv install
tgenv install
```

Some important environment variables are managed via direnv. Please ensure it's
working for you: https://direnv.net/docs/hook.html

## Onboarding

Each developer has to submit a simple change:

```
make terraform/env.$USER
git commit -am "feat: onboarding dev $USER"
```

## Usage

### Environment

To approximate the environment created by the tacos-gha system:

```
cd $tacos-gha
unset DIRENV_DIFF && cd -  # cd without reverting .envrc
direnv allow
```

### Plan & Apply

To do the common plan / review / apply cycle:

```
cd terraform/env.$USER
sudo-gcp terragrunt-noninteractive run-all plan -out plan
GETSENTRY_SAC_VERB=apply sudo-gcp terragrunt-noninteractive run-all apply plan
```

### Unlock All

Maybe this should be its own command ...

```
$TACOS_GHA_HOME/lib/tacos/locks |
  jq -r \
    ' select(.lock)
    | .slice as $slice
    | ( .Who
      | split("@")
      | [ "env"
        , "USER=\(.[0])"
        , "HOST=\(.[1])"
        , "tf-lock-release"
        , $slice
        ]
      | @sh
      )
    ' |
    GETSENTRY_SAC_VERB=apply sudo-gcp sh -ex
```

[install homebrew]: https://brew.sh/
