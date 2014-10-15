#!/usr/bin/env python
#
# Author: Rogerio Varalda - rogeriovaralda<at>gmail.com
#
# Quick fix for AWS ELBs SSL Security Policy preventing POODLE issue with SSL vunerability
#

from boto.ec2 import elb

def set_elb_policy(elbs):
    print "Updating ELB Policies..."
    for lb in elbs.get_all_load_balancers():
        for j in lb.listeners:
            if j[2] == 'HTTPS' or j[2] == 'SSL':
                print lb.name
                lb.create_lb_policy(policy_name='EELBSecurityPolicy-2014-10', policy_type='SSLNegotiationPolicyType', policy_attribute={'Reference-Security-Policy': 'ELBSecurityPolicy-2014-10'})
                lb.set_policies_of_listener(j[0], 'EELBSecurityPolicy-2014-10')


def print_policies(elbs):
    print "\nFixed Policies:"
    for i in elbs.get_all_load_balancers():
        for j in i.listeners:
            if j[2] == 'HTTPS' or j[2] == 'SSL':
                print i.name, i.policies


def main():
    regions = [ r for r in elb.regions() if r.name not in ['cn-north-1', 'us-gov-west-1'] ]

    for region in regions:
        print '\n' + region.name
        elbs = elb.connect_to_region(region.name)
        set_elb_policy(elbs)
        print_policies(elbs)



if __name__ == '__main__':
    main()