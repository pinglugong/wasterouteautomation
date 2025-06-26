from flask import Flask, request, jsonify
import ee
import os

app = Flask(__name__)

# Initialize Earth Engine
ee.Initialize(project= 'waste-route-automation-agent')

@app.route('/satellite', methods=['POST'])
def get_image():
    try:
        data = request.json
        bbox = data['boundingBox']
        
        # Create geometry from bounding box
        geometry = ee.Geometry.Rectangle([
            bbox['west'], 
            bbox['south'], 
            bbox['east'], 
            bbox['north']
        ])
        
        # Get satellite image
        image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(geometry) \
            .filterDate('2020-01-01', '2023-12-31') \
            .sort('CLOUD_COVER') \
            .first()
        
        # Get download URL
        url = image.getDownloadURL({
            'scale': 30,
            'region': geometry,
            'format': 'GEO_TIFF'
        })
        
        return jsonify({'image_url': url, 'status': 'success'})
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))