from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # http -> Django views is added by default
})
