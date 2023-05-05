import openstack

# Authentification auprès d'OpenStack
conn = openstack.connect(cloud='mycloud')

# Paramètres du réseau
network_name = 'my_network'
project_id = 'my_project'
subnet_cidr = '192.168.1.0/24'
subnet_gateway = '192.168.1.1'

# Création du réseau
network = conn.network.create_network(name=network_name, project_id=project_id)
subnet = conn.network.create_subnet(
    name=network_name + '_subnet', 
    network_id=network.id, 
    ip_version=4, 
    cidr=subnet_cidr, 
    gateway_ip=subnet_gateway
)

print('Le réseau {} a été créé avec succès'.format(network.name))
