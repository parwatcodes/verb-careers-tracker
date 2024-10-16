const jobElements = document.querySelectorAll('li[data-uri="job');
let jobs = [];

jobElements.forEach(job => {
  const title = job.querySelector('h3[data-ui="job-title').innerText;
  const link = job.querySelector('a').href;

  jobs.push({
    title,
    link
  });
});


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'getJobs') {
    sendResponse({ jobs });
  }
});
