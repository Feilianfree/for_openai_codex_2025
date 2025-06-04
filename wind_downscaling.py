# Wind field downscaling using bilinear interpolation.
# This script works with Python's standard library only.

from typing import List, Tuple
import math

Grid = List[List[float]]


def bilinear_interpolate(grid: Grid, scale_factor: int) -> Grid:
    """Upscale a 2D grid using bilinear interpolation.

    Args:
        grid: 2D list of floats representing a coarse grid.
        scale_factor: factor to increase resolution (e.g. 2 => 2x more rows/cols).

    Returns:
        new_grid: interpolated grid with size (rows*scale_factor, cols*scale_factor).
    """
    if scale_factor <= 1:
        raise ValueError("scale_factor must be > 1")

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    new_rows = rows * scale_factor
    new_cols = cols * scale_factor
    result: Grid = []

    for i in range(new_rows):
        row: List[float] = []
        for j in range(new_cols):
            src_x = j / scale_factor
            src_y = i / scale_factor
            x0 = int(math.floor(src_x))
            x1 = min(x0 + 1, cols - 1)
            y0 = int(math.floor(src_y))
            y1 = min(y0 + 1, rows - 1)

            dx = src_x - x0
            dy = src_y - y0

            v00 = grid[y0][x0]
            v10 = grid[y0][x1]
            v01 = grid[y1][x0]
            v11 = grid[y1][x1]

            value = (
                v00 * (1 - dx) * (1 - dy)
                + v10 * dx * (1 - dy)
                + v01 * (1 - dx) * dy
                + v11 * dx * dy
            )
            row.append(value)
        result.append(row)
    return result


def downscale_wind(u_grid: Grid, v_grid: Grid, scale_factor: int) -> Tuple[Grid, Grid]:
    """Downscale wind field (u and v components) via bilinear interpolation."""
    return (
        bilinear_interpolate(u_grid, scale_factor),
        bilinear_interpolate(v_grid, scale_factor),
    )


def _print_grid(grid: Grid) -> None:
    for row in grid:
        print(" ".join(f"{v:6.2f}" for v in row))


def main() -> None:
    """Demonstrate wind field downscaling on a small synthetic grid."""
    u_coarse = [
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 4.0, 5.0],
    ]
    v_coarse = [
        [0.5, 0.5, 0.5],
        [1.0, 1.0, 1.0],
        [1.5, 1.5, 1.5],
    ]

    scale = 2
    u_fine, v_fine = downscale_wind(u_coarse, v_coarse, scale)

    print("U component (coarse):")
    _print_grid(u_coarse)
    print("\nU component (downscaled):")
    _print_grid(u_fine)

    print("\nV component (coarse):")
    _print_grid(v_coarse)
    print("\nV component (downscaled):")
    _print_grid(v_fine)


if __name__ == "__main__":
    main()
