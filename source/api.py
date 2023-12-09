def location(world: 'World', x: float, y: float, z: float, yaw: float = 0, pitch: float = 0) -> 'Location':
    return Location(world, x, y, z, yaw, pitch)