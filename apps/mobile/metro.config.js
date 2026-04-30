const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Fix web module resolution
config.resolver.unstable_enablePackageExports = false;
config.resolver.platforms = ['ios', 'android', 'native', 'web'];

module.exports = config;
