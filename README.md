# Ansible playbook for AutomationLogic

## Description:

#### Please prepare a tarball that implements the steps below.

#### The solution should contain a Vagrantfile, all associated configuration management files, and a README that lists both the steps we should run to duplicate your solution and any assumed software version(s).

The solution should only require vagrant installed on the host machine with all additional software installed on the virtual machines.

* Create a Vagrantfile that creates a single machine using this box:https://vagrantcloud.com/puppetlabs/boxes/ubuntu-14.04-64-nocm
and installs the latest released version of your chosen configuration management tool.  
* Install the nginx webserver via configuration management.  
* Run a simple test using Vagrant's shell provisioner to ensure that nginx is listening on port 80  
* Again, using configuration management, update contents of /etc/sudoers file so that Vagrant user can sudo without a password and that anyone in the admin group can sudo with a password.  
* Make the solution idempotent so that re-running the provisioning step will not restart nginx unless changes have been made  
* Create a simple "Hello World" web application in your favourite language of choice.  
* Ensure your web application is available via the nginx instance.  
* Extend the Vagrantfile to deploy this webapp to two additional vagrant machines and then configure the nginx to load balance between them.  
* Test (in an automated fashion) that both app servers are working, and that the nginx is serving the content correctly.  

I’m interested in your working as much as your answers, so where you make a decision to go one way rather than another, please explain your thinking.
Your solution will be assessed on code quality and comprehensibility, not just on technical correctness.

Optional Extra credit:
* Have the webapp be dynamic - e.g. perform a db query for inclusion in the response (such as picking a random quote from a database) or calling an API of your choice(e.g. weather).  
* Any additional resources (e.g. a shared db server) should be set up by the Vagrant file 
* Include a section for possible improvements and compromises made during the development of your solution

## Usage:

Just type: 

```sh
vagrant up
```

All dependencies etc. will be installed. 
Vagrant will deploy 3 machines (`lb1`, `vm1`, `vm2`) the whole orchestration will be done from `lb1`.
`lb1` will deploy nginx instance that will load-balance traffic (basic load balancing) between `vm1` & `vm2`.

On VM1 and VM2 python webapp (flask - it will fetch random image from xkcd) will be deployed and it will be started (using `supervisord` on port 5000. It will be also available on port 80. 

Ansible will check if port 5000 is listening on `vm1` and `vm2`. The last task is to check if content is found on the `lb1` and `vm1` & `vm2`.


## Ansible variables:

I tried to make this playbook as much flexible as I could.

In `group_vars` directory we have 3 files:

* all
* lb
* website

`all` - those settings will be applied to every machine that is orchestratied using Ansible.

`lb` - those settings will be applied only to `lb` group (check `inventory` file)

`website` - those settings will be applied to `website` group (check `inventory` file)

#### all

```yaml
sudo_users:
  - { name: '%admin' }
  - { name: 'vagrant', nopasswd: yes }
```

`sudo_users` is responsible for managing sudo users. `name` is **required** and `nopasswd` is **optional**. 

#### lb

```yaml
nginx_config:
  proxy:
    name: vm1vm2
    tmpl: proxy.j2
    backend_port: 5000
    backend_group: website
    virhost: localhost

check_port:
  - { port: 80 }
```

`check_port` will check if the port is listening. `port` is **required** and `host` is **optional** (default: localhost)

`nginx_config` is used to generate nginx config:
each variable here is **required**

there are 2 `tmpl` (templates):
 * proxy.j2
 * webiste-backend.j2

I think the naming is intuitive and there is no need to explain this.


#### website

```yaml
supervisord:
  flask-app:
    name: random-xkcd
    host: 0.0.0.0
    port: 5000
    dir: /app/
    user: vagrant

content_check:
  - { host: 'http://10.0.0.10', cont: 'xkcd.com' }
  - { host: 'http://10.0.0.201:5000', cont: 'xkcd.com' }
  - { host: 'http://10.0.0.202:5000', cont: 'xkcd.com' }
  
nginx_config:
  default:
    tmpl: website-backend.j2
    backend_host: localhost
    listen_ip: default_server
    virhost: localhost  
    backend_port: 5000

check_port:
  - { port: 5000 }
```

`supervisord` is required for our webapp, it will spawn and supervise our webapp - in case of failure it will try to restart it.

Each variable is **required**

`content_check` will run from ansible host machine and will check if the content is available on the machine that is provided in `host` variable 

