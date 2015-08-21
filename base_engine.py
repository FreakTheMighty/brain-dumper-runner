import caffe
import numpy as np
import os

class Engine(object):

    BRAIN_DIR = '/brain'

    def build_params(self):
        params = {
            'caffemodel': None,
            'deploy_file': None,
            'mean': None,
            'labels_file': None
          }
        
        for filename in os.listdir('/brain'):
            full_path = os.path.join(Engine.BRAIN_DIR, filename)
            if filename.endswith('.caffemodel'):
                params['caffemodel'] = full_path
            elif filename == 'deploy.prototxt':
                params['deploy_file'] = full_path
            elif filename.endswith('.npy'):
                params['mean'] = np.load(full_path).mean(1).mean(1)
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
        deploy_file = params.pop('deploy_file')
        caffemodel = params.pop('caffemodel')
        label_path = params.pop('labels_file')
        self.labels = []
        if label_path:
            with open(label_path) as f:
                for line in f:
                    self.labels.append(line.strip())
            self.labels = np.array(self.labels)

        return caffe.Classifier(deploy_file, caffemodel, **params)

    def foward(self, inputs):
        input_image = caffe.io.load_image(inputs[0])
        scores = self.net.predict([input_image], oversample=True).flatten()
        if self.labels is not None:
            indices = (-scores).argsort()[:5]
            predictions = self.labels[indices]
            scores = scores[indices]
            return {'scores': zip(predictions.tolist(), scores.tolist())}
        else:
            return {'scores': scores}

