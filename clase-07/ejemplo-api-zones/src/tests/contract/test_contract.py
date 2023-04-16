# from pactman.verifier.verify import ProviderStateMissing

# def provider_state(name, **params):
#     if name == 'the user "pat" exists':
#         User.objects.create(username='pat', fullname=params['fullname'])
#     else:
#         raise ProviderStateMissing(name)

# def test_pacts(live_server, pact_verifier):
#     pact_verifier.verify(live_server.url, provider_state)
