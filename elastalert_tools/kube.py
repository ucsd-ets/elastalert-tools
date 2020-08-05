from kubernetes import client, config
from typing import List
import kubernetes, urllib3, copy, warnings, re

warnings.simplefilter("ignore", ResourceWarning)

class KubeConfigNotFound(Exception):
    pass

class K8SResourceNotFound(Exception):
    pass

def load_k8s(config_path):
    return config.load_kube_config(config_path)
    
def get_names(k8s_resources):
    return list(map(lambda resource: resource.metadata.name, k8s_resources))

class K8SAPI:
    def __init__(self):
        self.set_api()
        # TODO test whether connect() can be here

    def set_api(self):
        """Initialize the api
        """
        self._api = client.CoreV1Api()
    
    @property
    def namespaces(self) -> List[str]:
        """Get all namespaces

        Returns:
            str: namespaces
        """
        namespaces = self._api.list_namespace().items
        return [namespace.metadata.name for namespace in namespaces]

class Pod(K8SAPI):
    def __init__(self, podname):
        K8SAPI.__init__(self)
        self.podname = podname
        self._not_found_msg = 'Could not find active pod = '
        self._namespace = None
    
    @property
    def podname(self) -> str:
        return self._podname

    @podname.setter
    def podname(self, podname):
        ret = self._api.list_pod_for_all_namespaces(watch=False).items
        names = get_names(ret)
        
        if podname not in names:
            raise K8SResourceNotFound(f'podname = {podname} is not an active pod. Active pods = {names}')
        
        self._podname = podname
        
    @property
    def namespace(self) -> str:
        if self._namespace:
            return self._namespace

        ret = self._api.list_pod_for_all_namespaces(watch=False).items
        
        for pod in ret:
            if pod.metadata.name == self.podname:
                self._namespace = copy.deepcopy(str(pod.metadata.namespace))
                return self._namespace
        
        raise K8SResourceNotFound(self._not_found_msg + self.podname)
    
    @property
    def api(self):
        ret = self._api.list_pod_for_all_namespaces(watch=False).items
        names = get_names(ret)
        
        for name, pod in zip(names, ret):
            if name == self.podname:
                return pod
        
        raise K8SResourceNotFound(self._not_found_msg + self.podname)
    
    def kill(self):
        self._api.delete_namespaced_pod(self.podname, self.namespace, grace_period_seconds=0)

class Node(K8SAPI):
    def __init__(self, hostname):
        K8SAPI.__init__(self)
        self.hostname = hostname
        self._node = None
        
    @property
    def hostname(self):
        return self._hostname
    
    @hostname.setter
    def hostname(self, hostname):
        try:
            nodes = self._api.list_node().items
            names = get_names(nodes)
            if hostname not in names:
                raise K8SResourceNotFound(f'hostname = {hostname} is not a kubernetes node! Nodes = {names}')
            
            self._hostname = hostname

        except kubernetes.config.config_exception.ConfigException:
            raise kubernetes.config.config_exception.ConfigException(
                'Load the kubernetes config first. Example: elastalert_tools.kube.load_k8s(PATH_TO_CONFIG)'
            )
            
    @property
    def ip(self):
        node = self._api.read_node(self.hostname)
        return node.status.addresses[0].address
    
    def api(self):
        """Get underlying kubernetes node primitive (kubernetes.client.models.v1_node.V1Node) 

        Raises:
            K8SResourceNotFound: Not found node
        """
        nodes = self._api.list_node().items
        names = get_names(nodes)
        
        for name, node in zip(names, nodes):
            if name == self.hostname:
                return node

        raise K8SResourceNotFound(f'Could not find active node = {self.hostname}')

    def cordon(self):
        self._api.patch_node(self.hostname, {'spec': {'unschedulable': True}})
    
    def uncordon(self):
        self._api.patch_node(self.hostname, {'spec': {'unschedulable': False}})
    
    def get_pods(self, regex_filter: str ='') -> List[Pod]:
        """Get a list of running pods

        Args:
            regex_filter (str, optional): regex expression to filter out non-matching pod names. Defaults to ''.

        Returns:
            List[Pod]: List of pods
        """
        pods = self._api.list_pod_for_all_namespaces(watch=False).items
        
        host_pods = []
        for pod in pods:
            # FIXME list(filter) initial implementation of this failed
            if pod.status.host_ip == self.ip:
                host_pods.append(pod)

        # filter
        podnames = get_names(host_pods)
        r = re.compile(regex_filter)
        podnames = list(filter(r.match, podnames))
        
        return [Pod(podname) for podname in podnames]
    
class Nodes(K8SAPI):
    def __init__(self):
        K8SAPI.__init__(self)
        self.connect()
    
    def __len__(self):
        return len(self._nodes)
    
    def __iter__(self):
        for node in self._nodes:
            yield node
    
    def connect(self):
        nodes = self._api.list_node().items
        hostnames = get_names(nodes)
        
        self._nodes = [Node(hostname) for hostname in hostnames]