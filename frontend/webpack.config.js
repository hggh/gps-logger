const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        'path': path.resolve(__dirname, '..', 'gpslogger', 'logger',  'static'),
        'filename': 'bundle.js'
    },
    module: {
        rules: [
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader'
            ]
          }
        ],
        
    }
}