// Learn more https://docs.expo.io/guides/customizing-metro
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Support web
config.resolver.unstable_enablePackageExports = false;

module.exports = config;
