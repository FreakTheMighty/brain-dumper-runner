import caffe
import numpy as np

class Engine(object):

    BRAIN_DIR = '/brain'

    def build_params(self):
        params = {
            caffemodel: None,
            deploy_file: None,
            mean_file: None,
            labels_file: None
          }
        
        for filename in os.listdir('/brain'):
            full_path = os.path.join(Engine.BRAIN_DIR, filename)
            if filename.endswith('.caffemodel'):
                params['caffemodel'] = full_path
            elif filename == 'deploy.prototxt':
                params['deploy_file'] = full_path
            elif filename.endswith('.npy'):
                params['mean_file'] = np.load(full_path).mean(1).mean(1),
            elif filename == 'labels.txt':
                params['labels_file'] = full_path
            else:
                print 'Unknown file:', filename

        params['raw_scale'] = 255
        params['channel_swap'] = (2,1,0)
        params['image_dims'] = (256, 256)
                
        return params

    def load(self):
        params = self.build_params()
        return caffe.Classifier(params['deploy_file'], params['model_file'], **params)

    def foward(self, inputs):
        input_image = caffe.io.load_image(inputs[0])
        prediction = self.net.predict([input_image], oversample=True).flatten().tolist()
        return {'predictions': prediction}

