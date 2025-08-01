Post processing scripts for Cellpose-Sam or SwinCell inference output.

Workflow to compute cell count and histograms of gut cells:

1- Use combine_masks.py to remove cells that are located outside of organ.

2- Use compute_metrics_and_order.py to re-label a 3D mask to consecutive IDs, drop small objects, compute volumes, save CSV stats, and plot histogram.
