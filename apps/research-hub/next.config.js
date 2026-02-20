module.exports = {
  webpack: (config: any) => {
    config.resolve.fallback = {
      fs: false,
    };
    return config;
  },
};
