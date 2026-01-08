module.exports = {
  apps: [{
    name: 'espaluz-influencer',
    script: 'main.py',
    interpreter: '/home/ubuntu/espaluz-influencer-upgrade/venv/bin/python',
    cwd: '/home/ubuntu/espaluz-influencer-upgrade',
    env: {
      PYTHONUNBUFFERED: '1'
    },
    watch: false,
    autorestart: true,
    max_restarts: 10,
    restart_delay: 5000
  }]
};
