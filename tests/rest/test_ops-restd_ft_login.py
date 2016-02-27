import os
import sys
import time
import pytest
import subprocess
import shutil
import json
import httplib
import urllib
from opsvsi.docker import *
from opsvsi.opsvsitest import *
from opsvsiutils.systemutil import *
from opsvsiutils.restutils.utils import *
import ssl

NUM_OF_SWITCHES = 1
NUM_HOSTS_PER_SWITCH = 0


class myTopo(Topo):
    def build(self, hsts=0, sws=1, **_opts):

        self.hsts = hsts
        self.sws = sws
        switch = self.addSwitch("s1")


class configTest (OpsVsiTest):
    def setupNet(self):

        host_opts = self.getHostOpts()
        switch_opts = self.getSwitchOpts()
        ecmp_topo = myTopo(hsts=NUM_HOSTS_PER_SWITCH, sws=NUM_OF_SWITCHES,
                           hopts=host_opts, sopts=switch_opts)
        self.net = Mininet(ecmp_topo, switch=VsiOpenSwitch, host=Host,
                           link=OpsVsiLink, controller=None, build=True)
        self.SWITCH_IP = get_switch_ip(self.net.switches[0])
        self.URL = '/login'

    def verify_login(self):

        #POST
        _headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}
        # GET to fetch system info from the DB

        body = {'username': 'netop', 'password': 'netop'}
        response, response_data = execute_request(
            self.URL, "POST", urllib.urlencode(body),
            self.SWITCH_IP, True, _headers)
        assert response.status == httplib.OK, ("Wrong status code %s "
                                               % response.status)

        _headers = {'Cookie': response.getheader('set-cookie')}
        time.sleep(2)
        info('\n######### Running GET to fetch the system' +
             ' info from the DB ##########\n')

        _headers = {'Cookie': response.getheader('set-cookie')}
        time.sleep(2)

        status_code, response_data = execute_request(
            self.URL, "GET", json.dumps(""),
            self.SWITCH_IP, False, _headers)
        assert status_code == httplib.OK, ("Wrong status code %s "
                                           % status_code)

        time.sleep(2)

        info('\n######### Running GET to fetch the system info' +
             ' from the DB after removing the cookie ##########\n')

        # GET to fetch system info from the DB
        response, response_data = execute_request(
            self.URL, "GET", json.dumps(""),
            self.SWITCH_IP, True, None)
        assert response.status == httplib.UNAUTHORIZED, \
            ("Wrong status code %s " % response.status)

        assert response.status == 401

    def verify_fail_login(self):

        #POST
        _headers = {"Content-type": "application/x-www-form-urlencoded",
                    "Accept": "text/plain"}

        info('\n######### Running POST to fetch the cookie ##########\n')
        body = {'username': 'Ops', 'password': 'Ops'}
        response, response_data = execute_request(
            self.URL, "POST", urllib.urlencode(body),
            self.SWITCH_IP, True, _headers)
        assert response.status == httplib.UNAUTHORIZED, \
            ("Wrong status code %s " % response.status)

        _headers = {'Cookie': response.getheader('set-cookie')}
        time.sleep(2)
        info('\n######### Running GET to fetch the system' +
             ' info from the DB ##########\n')

        status_code, response_data = execute_request(
            self.URL, "GET", json.dumps(""),
            self.SWITCH_IP, False, None)
        assert response.status == httplib.UNAUTHORIZED, \
            ("Wrong status code %s " % response.status)
        time.sleep(2)

        info('\n######### Running GET to fetch the system info' +
             'from the DB after removing the cookie ##########\n')

        # GET to fetch system info from the DB

        response, response_data = execute_request(
            self.URL, "GET", json.dumps(""),
            self.SWITCH_IP, True, None)
        assert response.status == 401


class Test_config:
    def setup(self):
        pass

    def teardown(self):
        pass

    def setup_class(cls):
        cls.test_var = configTest()
        rest_sanity_check(cls.test_var.SWITCH_IP)

    def teardown_class(cls):
        Test_config.test_var.net.stop()

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def __del__(self):
        del self.test_var

    def test_run(self):
        self.test_var.verify_login()
        self.test_var.verify_fail_login()
