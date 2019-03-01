from histoslider.models.acquisition_2d_data import Acquisition2DData
from histoslider.slides.mcd.mcd_slide import McdSlide
from histoslider.models.workspace import Workspace


def test_models():
    workspace = Workspace("My Workspace")
    slide = McdSlide("Slide")
    slide2 = McdSlide("Slide 2")

    acq = Acquisition2DData("a1")
    acq2 = Acquisition2DData("a2")

    slide.add_acquisition2d(acq)
    slide2.add_acquisition2d(acq2)

    workspace.add_slide(slide)
    workspace.add_slide(slide2)
    json = workspace.to_json()

    w2 = Workspace.from_json(json)

    assert json == w2.to_json()


if __name__ == "__main__":
    test_models()
