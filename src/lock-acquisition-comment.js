module.exports = ({ github, context }) => {
  const lockObtained = JSON.parse(
    context.steps.lock_check.outputs.lock_obtained
  );
  comment(lockObtained, github);
};

function comment(github, lockObtained) {
  if (lockObtained) {
    github.rest.issues.createComment({
      issue_number: context.issue.number,
      owner: context.repo.owner,
      repo: context.repo.repo,
      // FIXME: need to let them know who has the lock, if you can
      body: "❌🔒 Unable to obtain lock",
    });
  } else {
    github.rest.issues.createComment({
      issue_number: context.issue.number,
      owner: context.repo.owner,
      repo: context.repo.repo,
      body: "✅🔒 Obtained lock",
    });
  }
}
