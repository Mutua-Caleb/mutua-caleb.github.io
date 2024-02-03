document.getElementsByClassName('dark-mode-button')[0].onclick = function() {
    darkmode()
}
function darkmode() {
    let enabled = localStorage.getItem('dark-mode');
    const iconDark = document.getElementById('icon-dark');
    const iconLight = document.getElementById('icon-light');
  
    if (enabled === null) {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          enable();
      }
    } else if (enabled === 'true') {
      enable();
    }
  
    if (localStorage.getItem('dark-mode') === 'false') {
        enable();
    } else {
        disable();
    }
  
    // Toggle icons
    if (localStorage.getItem('dark-mode') === 'true') {
      iconDark.style.display = 'none';
      iconLight.style.display = 'inline';
    } else {
      iconDark.style.display = 'inline';
      iconLight.style.display = 'none';
    }
  }
  function enable()  {
    DarkReader.setFetchMethod(window.fetch)
    DarkReader.enable();
    localStorage.setItem('dark-mode', 'true');
  }
  
  function disable() {
    DarkReader.disable();
    localStorage.setItem('dark-mode', 'false');
  }