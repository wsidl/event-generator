from event_gen.config import model
from event_gen.generators import generators

from functools import partial

from pytest import mark

Prop_Def = partial(model.PropertyDefinition, name_="test")


def test_load_default_generator():
    base_def = Prop_Def(type="string", **generators.GENERATORS["string"][0])
    prop_def = Prop_Def(type="string")
    str_gen = generators.load_generator(None, prop_def)
    exp_gen = generators.string_generator(None, base_def)
    assert str_gen.__qualname__ == exp_gen.__qualname__, "Load Generator should return the String Generator"


@generators.register_generator("test", {"random": "value"})
def random_generator_type(root_obj, cfg: model.PropertyDefinition):
    def _gen():
        return 1, "test", cfg.prop_config
    return _gen


def test_register_generator():
    prop_def = Prop_Def(type="test")
    exp_gen = random_generator_type(None, prop_def)
    try:
        test_gen = generators.load_generator(None, prop_def)
    except KeyError:
        raise ValueError("Should have found a 'test' generator")
    assert test_gen.__qualname__ == exp_gen.__qualname__, "Should have returned the 'test' generator"
