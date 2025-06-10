const Koop = require('@koopjs/koop-core');
const provider = require('@koopjs/provider-file-geojson');
const path = require('path');
const koop = new Koop({ logLevel: 'debug' });
const output = require('koop-output-geojson');

// const auth = require('@koopjs/auth-direct-file')(
//   'pass-in-your-secret',
//   `${__dirname}/user-store.json`
// );

// koop.register(auth);
koop.register(output);
koop.register(provider, { dataDir: './provider-data' });

// Serve static files
koop.server.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Service catalog endpoint
koop.server.get('/catalog', (req, res) => {
  const fs = require('fs');
  const dataDir = path.join(__dirname, 'provider-data');
  
  fs.readdir(dataDir, (err, files) => {
    if (err) {
      return res.status(500).json({ error: 'Unable to read data directory' });
    }
    
    const geojsonFiles = files
      .filter(file => file.endsWith('.geojson'))
      .map(file => {
        const layerId = path.basename(file, '.geojson');
        return {
          id: layerId,
          name: layerId.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
          type: 'FeatureServer',
          url: `/file-geojson/rest/services/${layerId}/FeatureServer`,
          queryUrl: `/file-geojson/rest/services/${layerId}/FeatureServer/0/query`
        };
      });
    
    res.json({
      services: geojsonFiles,
      count: geojsonFiles.length
    });
  });
});

koop.server.listen(process.env.PORT || 8080);
