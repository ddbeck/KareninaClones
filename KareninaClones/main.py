# -*- coding: utf-8 -*-

import json
import sys

import click
import twython

from clones import karenina_clone


def oauth_dance(auth_info):
    # set up
    pre_auth_twitter = twython.Twython(auth_info['consumer_key'],
                                       auth_info['consumer_secret'])
    twitter_auth = pre_auth_twitter.get_authentication_tokens()

    # prompt user to go to web and get verifier code
    click.echo("Open: {}".format(twitter_auth['auth_url']))
    verifier = click.prompt("Please enter the code provided by Twitter")

    post_auth_twitter = twython.Twython(auth_info['consumer_key'],
                                        auth_info['consumer_secret'],
                                        twitter_auth['oauth_token'],
                                        twitter_auth['oauth_token_secret'])
    access_info = post_auth_twitter.get_authorized_tokens(verifier)

    click.echo("")
    click.echo("Access key: {}".format(access_info['oauth_token']))
    click.echo("Access secret: {}".format(access_info['oauth_token_secret']))


def validate_keyfile(ctx, param, value):
    if value is not None:
        try:
            auth_info = json.load(value)['twitter']
        except:
            ctx.echo('A valid JSON keyfile is required!')
            raise
        return auth_info
    else:
        return value


@click.command()
@click.option('--tweet/--no-tweet',
              help="Post/do not post to Twitter. Defaults to not posting.",
              default=False)
@click.option('--inaugural', default=False, is_flag=True,
              help="Tweet the first tweet.")
@click.option('--keyfile', 'auth_info', type=click.File('r'),
              callback=validate_keyfile,
              help='JSON file with Twitter keys and secrets.')
@click.option('--request-access', default=False, is_flag=True,
              help='Request access key and secret.')
def main(tweet, inaugural, auth_info, request_access):
    if auth_info is None and (tweet or request_access):
        click.echo("Twitter operations require a valid keyfile!")
        sys.exit(1)

    if request_access:
        oauth_dance(auth_info)
        sys.exit()

    if inaugural:
        clone = karenina_clone(nouns=['family'], adjectives=['happy'])
    else:
        clone = karenina_clone()

    if tweet:
        twitter = twython.Twython(auth_info['consumer_key'],
                                  auth_info['consumer_secret'],
                                  auth_info['access_key'],
                                  auth_info['access_secret'])
        twitter.update_status(status=clone)
    else:
        click.echo(clone)


if __name__ == '__main__':
    main()
