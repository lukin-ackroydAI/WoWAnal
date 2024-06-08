const { execSync } = require('child_process');

try {
  console.log('Pulling latest code...');
  execSync('git pull origin main', { stdio: 'inherit' });
  console.log('Repository updated successfully.');
} catch (error) {
  console.error(`Failed to update repository: ${error.message}`);
  process.exit(1);
}
