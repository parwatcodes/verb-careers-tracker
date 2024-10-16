document.addEventListener('DOMContentLoaded', function() {
  // Request job data from the content script
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: getJobs
    }, (results) => {
      if (results && results[0].result.jobs.length > 0) {
        const jobList = document.getElementById('job-list');
        results[0].result.jobs.forEach(job => {
          let li = document.createElement('li');
          li.innerHTML = `<a href="${job.link}" target="_blank">${job.title}</a>`;
          jobList.appendChild(li);
        });
      } else {
        document.getElementById('job-list').innerText = "No jobs found.";
      }
    });
  });
});

function getJobs() {
  const jobElements = document.querySelectorAll('li[data-ui="job"]');
  let jobs = [];

  jobElements.forEach(job => {
    const title = job.querySelector('h3[data-ui="job-title"]').innerText;
    const link = job.querySelector('a').href;

    jobs.push({
      title: title,
      link: link
    });
  });

  return { jobs: jobs };
}
