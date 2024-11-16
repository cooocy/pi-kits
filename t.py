import l

L1 = l.get_logger('self_keeping')
L2 = l.get_logger('self_keeping')

L1.info('111')
L1.info('222')
L2.info('333')
L2.info('444')
l.get_logger().info('555')
print(L1 is L2)
