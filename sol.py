import solara
import tempfile


data_dir = tempfile.gettempdir()
files = ['jw02727-o002_t062_nircam_clear-f090w_i2d.fits',
        'jw02727-o002_t062_nircam_clear-f277w_i2d.fits',
        ]

for fn in files:
    uri = f"mast:JWST/product/{fn}"
    from astroquery.mast import Observations
    Observations.download_file(uri, local_path=f'{data_dir}/{fn}')


@solara.component
def Page():
    with solara.Column():
        from jdaviz import Imviz
        import ipysplitpanes
        import ipygoldenlayout
        from jdaviz.app import custom_components
        import os
        import ipyvue
        import jdaviz

        ipysplitpanes.SplitPanes()
        ipygoldenlayout.GoldenLayout()
        for name, path in custom_components.items():
            ipyvue.register_component_from_file(None, name,
                                                os.path.join(os.path.dirname(jdaviz.__file__), path))

        ipyvue.register_component_from_file('g-viewer-tab', "container.vue", jdaviz.__file__)

        imviz = Imviz()
        for fn in files:
            imviz.load_data(f'{data_dir}/{fn}')
        display(imviz.app)
