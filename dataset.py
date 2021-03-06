import torch
from torch.utils.data import Dataset
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

class UCIAdult(Dataset):
    def __init__(self,root,train=True):
        super(UCIAdult,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        # 65, Private, 198766, Masters, 14, Married-civ-spouse, Sales, Husband, White, Male, 20051, 0, 40, United-States, >50K
        self.fields = [{'type':'num'},
                       {'type':'cate','choices':['unk','Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked']},
                       {'type': 'num'},
                       {'type': 'cate', 'choices': ['unk','Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool']},
                       {'type': 'num'},
                       {'type': 'cate', 'choices': ['unk','Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse' ]},
                       {'type': 'cate', 'choices': ['unk','Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces' ]},
                       {'type': 'cate', 'choices': ['unk', 'Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried']},
                       {'type': 'cate', 'choices': ['unk', 'White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black']},
                       {'type': 'cate', 'choices': ['unk', 'Female', 'Male']},
                       {'type': 'num'},
                       {'type': 'num'},
                       {'type': 'num'},
                       {'type': 'cate', 'choices': ['unk', 'United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands']},
                       ]

        for field in self.fields:
            if field['type'] == 'cate':
                field['w2i'] = dict([(w,i) for i,w in enumerate(field['choices'])])

        self.X, self.y = self.load_data(root,train)


    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)


    def load_data(self,root,train):
        if train:
            data_path = os.path.join(root,"adult.data")
        else:
            data_path = os.path.join(root, "adult.test")

        with open(data_path) as f:
            rows = [ [ fv.strip() for fv in row.strip().split(",")] for row in f.readlines() if len(row.strip()) > 0 and not row.startswith("|")]
        n_datas = len(rows)
        X_dim = np.sum([ 1 if field['type']=='num' else len(field['choices']) for field in self.fields])
        X = np.zeros((n_datas, X_dim), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            assert len(row) == 15
            foffset = 0
            for j in range(14):
                if self.fields[j]['type'] == 'num':
                    fdim=1
                    X[i, foffset] = float(row[j])
                else:
                    fdim = len(self.fields[j]['choices'])
                    hit = self.fields[j]['w2i'].get(row[j],0)
                    X[i, foffset+hit] = 1
                foffset += fdim

            y[i] = 0 if row[-1].strip().startswith("<=50K") else 1

        X_min = np.array([[17.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 12285.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        X_max = np.array([[90.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1484705.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 16.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 99999.0, 4356.0, 99.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        X = (X - X_min) / np.clip((X_max - X_min), a_min=1e-6, a_max=None)

        #print([float(i) for i in np.min(X, axis=0)])
        #print([float(i) for i in np.max(X, axis=0)])


        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X, y


class UCILetter(Dataset):
    def __init__(self,root,train=True):
        super(UCILetter,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)


    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)

    def load_data(self,root,train):
        data_path = os.path.join(root, "letter-recognition.data")
        with open(data_path) as f:
            rows = [[ item.strip() for item in row.strip().split(',')] for row in f.readlines()]
        if train:
            rows = rows[:16000]
        else:
            rows = rows[16000:]

        n_datas = len(rows)
        X = np.zeros((n_datas, 16), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[1:]))
            y[i] = ord(row[0]) - ord('A')

        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y


class UCIYeast(Dataset):
    def __init__(self,root,train=True):
        super(UCIYeast,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.labels = ['CYT','NUC','MIT','ME3','ME2','ME1','EXC','VAC','POX','ERL']
        self.labels2idx = dict([ (label,i) for i,label in enumerate(self.labels)])

        self.X, self.y = self.load_data(root,train)


    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)


    def _load_data(self,data_path):
        with open(data_path) as f:
            rows = [ row.strip().split() for row in f.readlines()]
        n_datas = len(rows)
        X = np.zeros((n_datas, 8), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[1:-1]))
            y[i] = self.labels2idx[row[-1]]
        return X,y

    def _write_data(self, X, y, data_path):
        with open(data_path,'w') as f:
            for X_, y_ in zip(X,y):
                feat = ' '.join([str(x) for x in X_])
                f.write('placeholder %s %s\n'%(feat,self.labels[y_]))

    def load_data(self,root,train):
        if not os.path.exists(os.path.join(root, "yeast.train")) or \
            not os.path.exists(os.path.join(root, "yeast.test")):
            data_path = os.path.join(root, "yeast.data")
            X,y = self._load_data(data_path)
            n_datas = len(y)
            train_idx, test_idx = train_test_split(range(n_datas), random_state=0, train_size=0.7, stratify=y)
            self._write_data(X[train_idx],y[train_idx],os.path.join(root, "yeast.train"))
            self._write_data(X[test_idx], y[test_idx], os.path.join(root, "yeast.test"))

        if train:
            data_path = os.path.join(root, "yeast.train")
        else:
            data_path = os.path.join(root, "yeast.test")

        X, y = self._load_data(data_path)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y

class UCIIsolet5(Dataset):
    def __init__(self,root,train=True):
        super(UCIIsolet5,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)


    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)


    def _load_data(self,data_path):
        with open(data_path) as f:
            rows = [row.strip().split(', ') for row in f.readlines()]
        n_datas = len(rows)
        X = np.zeros((n_datas, 617), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[:-1]))
            if row[-1][:-1].isdigit():
                y[i] = int(row[-1][:-1])
            else: y[i] = 1
        return X,y
    
    def _write_data(self, X, y, data_path):
        with open(data_path,'w') as f:
            for X_, y_ in zip(X,y):
                feat = ', '.join([str(x) for x in X_])
                f.write('%s, %s.\n'%(feat,y_))

    def load_data(self,root,train):
        if not os.path.exists(os.path.join(root, "isolet5.train")) or \
            not os.path.exists(os.path.join(root, "isolet5.test")):
            data_path = os.path.join(root, "isolet5.data")
            X,y = self._load_data(data_path)
            n_datas = len(y)
            train_idx, test_idx = train_test_split(range(n_datas), random_state=0, train_size=0.7, stratify=y)
            self._write_data(X[train_idx],y[train_idx],os.path.join(root, "isolet5.train"))
            self._write_data(X[test_idx], y[test_idx], os.path.join(root, "isolet5.test"))

        if train:
            data_path = os.path.join(root, "isolet5.train")
        else:
            data_path = os.path.join(root, "isolet5.test")

        X, y = self._load_data(data_path)
        X = preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y
    
class UCISecom(Dataset):
    def __init__(self,root,train=True):
        super(UCISecom,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)


    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)


    def _load_data(self,data_path,label_path):
        with open(data_path) as f:
            rows = [ row.strip().split() for row in f.readlines()]
        with open(label_path) as f:
            self.labels = [ row.split()[0] for row in f.readlines()]
        print(self.labels)
        n_datas = len(rows)
        X = np.zeros((n_datas, 591), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            for j in range(len(row)):
                if row[j] == 'NaN':
                    if i > 0:
                        X[i,j] = X[i-1, j]
                    elif i < n_datas:
                        X[i,j] = X[i+1, j]
                else:
                    X[i,j] = float(row[j])
            if self.labels[i] == '1':
                y[i] = 1
        return X,y

    def _write_data(self, X, y, data_path, label_path):
        with open(data_path,'w') as f:
            for X_, y_ in zip(X,y):
                feat = ' '.join([str(x) for x in X_])
                f.write('%s\n'%(feat))
        with open(label_path,'w') as f:
            for X_, y_ in zip(X,y):
                f.write('%s\n'%(y_))

    def load_data(self,root,train):
        if not os.path.exists(os.path.join(root, "secom.train")) or \
            not os.path.exists(os.path.join(root, "secom.test")):
            data_path = os.path.join(root, "secom.data")
            label_path = os.path.join(root, "secom_labels.data")
            X,y = self._load_data(data_path, label_path)
            n_datas = len(y)
            train_idx, test_idx = train_test_split(range(n_datas), train_size=0.7,stratify=y)
            self._write_data(X[train_idx],y[train_idx],os.path.join(root,"secom.train"),os.path.join(root,"secom_label.train"))
            self._write_data(X[test_idx], y[test_idx], os.path.join(root, "secom.test"),os.path.join(root, "secom_label.test"))

        if train:
            data_path = os.path.join(root, "secom.train")
            label_path = os.path.join(root, "secom_label.train")
        else:
            data_path = os.path.join(root, "secom.test")
            label_path = os.path.join(root, "secom_label.test")

        X, y = self._load_data(data_path,label_path)
        X = preprocessing.normalize(X)
        X = preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y
    
class UCIGisette(Dataset):
    def __init__(self,root,train=True):
        super(UCIGisette,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)

    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)

    def load_data(self,root,train):
        if train:
            data_path = os.path.join(root, "gisette_train.data")
            label_path = os.path.join(root, "gisette_train.labels")
        else:
            data_path = os.path.join(root, "gisette_valid.data")
            label_path = os.path.join(root, "gisette_valid.labels")            
        with open(data_path) as f:
            rows = [[ item.strip() for item in row.strip().split()] for row in f.readlines()]
        with open(label_path) as f:
            labels = [int(row.strip()) for row in f.readlines()]
        n_datas = len(rows)
        X = np.zeros((n_datas, 5000), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[:]))
        for j, label in enumerate(labels):
            y[i] = max(0,labels[i])
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y

class UCIBreastcancer(Dataset):
    def __init__(self,root,train=True):
        super(UCIBreastcancer,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)

    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)

    def _load_data(self,data_path):
        with open(data_path) as f:
            rows = [ row.strip().split(',') for row in f.readlines()]
        n_datas = len(rows)
        X = np.zeros((n_datas, 30), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[2:]))
            y[i] = 1 if row[1]=='M' else 0
        return X,y

    def _write_data(self, X, y, data_path):
        labels = ['B','M']
        with open(data_path,'w') as f:
            for X_, y_ in zip(X,y):
                feat = ','.join([str(x) for x in X_])
                f.write('placeholder,%s,%s\n'%(labels[y_],feat))

    def load_data(self,root,train):
        if not os.path.exists(os.path.join(root, "breast.train")) or \
            not os.path.exists(os.path.join(root, "breast.test")):
            data_path = os.path.join(root, "breast_cancer.data")
            X,y = self._load_data(data_path)
            n_datas = len(y)
            train_idx, test_idx = train_test_split(range(n_datas), train_size=0.7)
            self._write_data(X[train_idx],y[train_idx],os.path.join(root, "breast.train"))
            self._write_data(X[test_idx], y[test_idx], os.path.join(root, "breast.test"))

        if train:
            data_path = os.path.join(root, "breast.train")
        else:
            data_path = os.path.join(root, "breast.test")

        X, y = self._load_data(data_path)
        X = preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y
    
class UCIMadelon(Dataset):
    def __init__(self,root,train=True):
        super(UCIMadelon,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)

    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)

    def load_data(self,root,train):
        if train:
            data_path = os.path.join(root, "madelon_train.data")
            label_path = os.path.join(root, "madelon_train.labels")
        else:
            data_path = os.path.join(root, "madelon_valid.data")
            label_path = os.path.join(root, "madelon_valid.labels")            
        with open(data_path) as f:
            rows = [[item.strip() for item in row.strip().split()] for row in f.readlines()]
        with open(label_path) as f:
            labels = [int(row.strip()) for row in f.readlines()]
        n_datas = len(rows)

        X = np.zeros((n_datas, 500), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            X[i, :] = list(map(float, row[:]))
        for j, label in enumerate(labels):
            y[j] = max(0,int(label))
            
#         X = preprocessing.normalize(X)
        X = preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y
    
class UCIArrhythmia(Dataset):
    def __init__(self,root,train=True):
        super(UCIArrhythmia,self).__init__()
        self.root = os.path.expanduser(root)
        self.train = train
        self.X, self.y = self.load_data(root,train)

    def __getitem__(self, index):
        return (self.X[index],self.y[index])

    def __len__(self):
        return len(self.X)

    def _load_data(self,data_path):
        with open(data_path) as f:
            rows = [ row.strip().split(',') for row in f.readlines()]
        n_datas = len(rows)

        X = np.zeros((n_datas, 279), dtype=np.float32)
        y = np.zeros(n_datas, dtype=np.int32)
        for i, row in enumerate(rows):
            for j in range(1, len(row)-1):
                if row[j] == '?':
                    if i > 0:
                        X[i,j] = X[i-1, j]
                    elif i < n_datas:
                        X[i,j] = X[i+1, j]
                else:
                    X[i,j] = float(row[j])

            y[i] = float(row[-1])
        self.labels = y
        return X,y

    def _write_data(self, X, y, data_path):
        with open(data_path,'w') as f:
            for X_, y_ in zip(X,y):
                feat = ','.join([str(x) for x in X_])
                f.write('placeholder %s,%s\n'%(feat,self.labels[y_]))

    def load_data(self,root,train):
        if not os.path.exists(os.path.join(root, "arrhythmia.train")) or \
            not os.path.exists(os.path.join(root, "arrhythmia.test")):
            data_path = os.path.join(root, "arrhythmia.data")
            X,y = self._load_data(data_path)
            n_datas = len(y)
            train_idx, test_idx = train_test_split(range(n_datas), random_state=0, train_size=0.7, stratify=y)
            self._write_data(X[train_idx],y[train_idx],os.path.join(root, "arrhythmia.train"))
            self._write_data(X[test_idx], y[test_idx], os.path.join(root, "arrhythmia.test"))

        if train:
            data_path = os.path.join(root, "arrhythmia.train")
        else:
            data_path = os.path.join(root, "arrhythmia.test")

        X, y = self._load_data(data_path)
        X = preprocessing.normalize(X)
        X = preprocessing.scale(X, axis=0, with_mean=True,with_std=True,copy=True)
        X = torch.from_numpy(X).type(torch.FloatTensor)
        y = torch.from_numpy(y).type(torch.IntTensor)
        return X,y
 
