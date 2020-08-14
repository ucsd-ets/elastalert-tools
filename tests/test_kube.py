import unittest, random
from kubernetes import client
from shutil import which

from elastalert_tools.kube import *

def manifest_with_command(name, command):
    return {
        'apiVersion': 'v1',
        'kind': 'Pod',
        'metadata': {
            'name': name
        },
        'spec': {
            'containers': [{
                'image': 'busybox',
                'name': 'sleep',
                "args": [
                    "/bin/sh",
                    "-c",
                    command
                ]
            }]
        }
    }

CONFIG_PATH = '/home/kube/.kube/config'

KUBE_DOES_NOT_EXIST = which('kubectl') is None
@unittest.skipIf(KUBE_DOES_NOT_EXIST, 'kubernetes cluster not available')
class TestK8SAPI(unittest.TestCase):
    def setUp(self):
        load_k8s(CONFIG_PATH)
        self.api = K8SAPI()
    
    def test_namespaces(self):
        assert self.api.namespaces is not None, 'namespaces doesnt exist'
        assert 'default' in self.api.namespaces, f'default doesnt exist = {self.api.namespaces}'
        
@unittest.skipIf(KUBE_DOES_NOT_EXIST, 'kubernetes cluster not available')
class TestPod(unittest.TestCase):
    def setUp(self):
        load_k8s(CONFIG_PATH)
        self.api = client.CoreV1Api()
        pods = self.api.list_pod_for_all_namespaces(watch=False).items
        self.podnames = get_names(pods)
        self.pod = Pod(self.podnames[0])
        
    def tearDown(self):
        self.api.api_client.close()
        del self.pod
        del self.api
    
    def test_pod_init(self):
        assert self.pod.podname == self.podnames[0], 'podname not set'
        
    def test_namespace(self):
        assert self.pod.namespace is not None, f'namespace not set = {self.pod.namespace}'
    
    def test_api(self):
        assert self.pod.api is not None, f'underlying api is not accessible'
        
    def test_kill(self):
        name = 'busybox-test'
        pod_manifest = manifest_with_command(name, "while true;do date;sleep 100; done")
        resp = self.api.create_namespaced_pod(body=pod_manifest,
                                         namespace='default')

        pod = Pod(name)
        pod.kill()
        
        with self.assertRaises(K8SResourceNotFound):
            Pod(name)

@unittest.skipIf(KUBE_DOES_NOT_EXIST, 'kubernetes cluster not available')
class TestNode(unittest.TestCase):
    def setUp(self):
        load_k8s(CONFIG_PATH)
        self.api = client.CoreV1Api()
        self.nodes = self.api.list_node().items
        self.ip_addresses = [node.status.addresses[0].address for node in self.nodes]
        self.hostnames = [node.status.addresses[1].address for node in self.nodes]
        self.hostname = random.choice(self.hostnames)
        self.node = Node(self.hostname)
        
    def get_worker_node(self):
        nodes = self.api.list_node().items
        for node in nodes:
            if 'node-role.kubernetes.io/master' not in dict(node.metadata.labels).keys():
                return node

    def test_init(self):
        assert self.node.hostname == self.hostname, 'host name didnt set'
        
        with self.assertRaises(K8SResourceNotFound):
            Node('fakenode')
    
    def test_ip(self):
        assert self.node.ip in self.ip_addresses
        
    def test_hostname(self):
        assert self.node.hostname == self.hostname
        
    def cordon(self):
        """Used for testing cordon and uncordon below"""
        
        # find worker node
        node = self.get_worker_node()
        hostname = node.status.addresses[1].address
        worker = Node(hostname)
        worker.cordon()
        node = self.get_worker_node()
        assert node.spec.unschedulable == True, 'Node is schedulable'
        
        return {'worker': worker, 'hostname': hostname}

    def test_cordon(self):
        dat = self.cordon()
        
        # reset
        self.api.patch_node(dat['hostname'], {'spec': {'unschedulable': False}})
    
    def test_uncordon(self):
        dat = self.cordon()
        worker = dat['worker']
        worker.uncordon()
        
        node = self.get_worker_node()
        assert node.spec.unschedulable is None, 'Node is unschedulable'

    def test_get_pods(self):
        pods = self.node.get_pods()
        
        for pod in pods:
            assert isinstance(pod, Pod), 'pod is not a pod'
            
        assert len(pods) > 1, ''
        
        # test filtering
        pods = self.node.get_pods('kube-proxy-')
        nodes = self.api.list_node().items
        
        assert len(pods) == 1, f'There shoudl be only 1 kube_proxy pod on every node. Length = {len(pods)}'