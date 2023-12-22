module.exports = ({ github, context, lockResults }) => {
  comment(github, context, JSON.parse(lockResults));
};

function comment(github, context, lockResults) {
  let commentBody = "Lock Summary:\n\n";

  for (const result of lockResults) {
    // FIXME: need to let them know who has the lock, if you can
    commentBody += `- Slice: ${result.slice}, Lock Obtained: ${result.lock_obtained}\n`;
  }
  
  github.rest.issues.createComment({
    issue_number: context.issue.number,
      owner: context.repo.owner,
      repo: context.repo.repo,
      body: commentBody,
  });
}
