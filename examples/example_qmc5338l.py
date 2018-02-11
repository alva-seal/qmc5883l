import qmc5883l

mag_sens = qmc5883l.QML5883L()

[x, y, z] = mag_sens.get_magnet()
