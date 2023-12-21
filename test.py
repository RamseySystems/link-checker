from reformatter import functions as fn

standards = {
    'Standard Name': {
        'path.to.node': 'http://www.someurl.com',
        'another.path': 'http://www.anotherURL.com'
    },
    'Another Standard': {
        'path.to.url': 'http://www.theurl.com',
        'path3.to.pathy': 'http://www.rtg.cod'
    }
}

email = fn.render_email('/Users/frankiehadwick/Documents/Link Checker/reformatter/templates',
                        'email.jinja', 
                        standards,
                        'Failed URL\'s')


fn.send_email('Testing',
              email,
              'frankiepaulhadwick@gmail.com',
              'frankie@ramseysystems.co.uk',
              'addt dubr qlnc zcdv')