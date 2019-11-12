import click

@click.command()
@click.argument('a')
@click.argument('b')
def calc_prod(a,b):
    '''
    Use: multiply a (float) times b (floats)
    '''
    result = a*b
    return result

calc_prod()

# need to know whether you have options or arguments
#arguments are mandatory
# arguments don't have defaults


# would normally use parameters, results, etc for web things