from dataclasses import dataclass
from drafter import *
from bakery import assert_equal

@dataclass
class Calculation:
    force: float
    area: float
    yield_strength: float
    stress: float
    factor_of_safety: float
    target_fos: float
    assessment: str
    
@dataclass
class State:
    force_input: str
    area_input: str
    yield_strength: str
    target_fos_input: str
    calculations: list[Calculation]
    
def calculate_stress(force: float, area: float) -> float:
    return force / area


def calculate_factor_of_safety(yield_strength: float, stress: float) -> float:
    return yield_strength / stress


def check_target(factor_of_safety: float, target_fos: float) -> str:
    if factor_of_safety >= target_fos:
        return "Your target factor of safety was met!"
    else:
        return "Your target factor of safety was not met."
    
assert_equal(calculate_stress(100, 20), 5.0)
assert_equal(calculate_stress(75, 10), 7.5)

assert_equal(calculate_factor_of_safety(250, 5), 50.0)
assert_equal(calculate_factor_of_safety(200, 8), 25.0)

assert_equal(check_target(3.0, 2.5), "Your target factor of safety was met!")
assert_equal(check_target(1.5, 2.0), "Your target factor of safety was not met.")
    
@route
def index(state: State) -> Page:
    return Page(state, [
        "Normal Stress and Factor of Safety Calculator",
        "\n",
        "Welcome! This calculator helps you calculate normal stress and determine the factor of safety for a material.",
        "\n",
        "Use this website to enter your information and see your results.",
        Button("Open Calculator", "calculator"),
        Button("View History", "history"),
        Button("About", "about")
    ])
@route
def calculator(state: State) -> Page:
    return Page(state, [
        "Normal Stress Calculator",
        "\n",
        "Enter the following information:",
        "\n",
        "Applied Force (N):",
        TextBox("force_input"),
        "\n",
        "Cross-Sectional Area (mm^2):",
        TextBox("area_input"),
        "\n",
        "Yield Strength (MPa):",
        TextBox("yield_strength"),
        "\n",
        "Target Factor of Safety:",
        TextBox("target_fos_input"),
        "\n",
        Button("Submit", "calculate"),
        Button("Back Home", "index"),
    ])
@route
def calculate(state: State, force_input: str, area_input: str,
              yield_strength: str, target_fos_input: str) -> Page:

    try:
        force = float(force_input)
        area = float(area_input)
        yield_strength = float(yield_strength)
        target_fos = float(target_fos_input)

    except ValueError:
        return Page(state, [
            "Please enter valid numbers.",
            Button("Try Again", "calculator")
        ])

    if force <= 0 or area <= 0 or yield_strength <= 0 or target_fos <= 0:
        return Page(state, [
        "All inputs must be greater than zero.",
        Button("Try Again", "calculator")
    ])

    stress = calculate_stress(force, area)

    factor_of_safety = calculate_factor_of_safety(yield_strength, stress)

    assessment = check_target(factor_of_safety, target_fos)

    calculation = Calculation(
        force,
        area,
        yield_strength,
        stress,
        factor_of_safety,
        target_fos,
        assessment
    )

    state.calculations.append(calculation)

    return Page(state, [
    "Your calculation is complete!",
    "\n",
    Button("View Results", "results"),
    Button("Home", "index")
    ])
@route
def results(state: State) -> Page:
    calculation = state.calculations[-1]

    return Page(state, [
        "Calculation Results",
        "\n",
        "Applied Force: " + str(calculation.force) + " N",
        "\n",
        "Cross-Sectional Area: " + str(calculation.area) + " mm^2",
        "\n",
        "Yield Strength: " + str(calculation.yield_strength) + " MPa",
        "\n",
        "Normal Stress: " + str(round(calculation.stress, 2)) + " MPa",
        "\n",
        "Factor of Safety: " + str(round(calculation.factor_of_safety, 2)),
        "\n",
        "Target Factor of Safety: " + str(calculation.target_fos),
        "\n",
        calculation.assessment,
        "\n",
        Button("Calculate Again", "calculator"),
        Button("View History", "history"),
        Button("Home", "index")
    ])
@route
def history(state: State) -> Page:
    content = [
        "Calculation History",
        "\n"
    ]

    if len(state.calculations) == 0:
        content.append("No calculations have been made yet.")
    else:
        for index in range(len(state.calculations)):
            calculation = state.calculations[index]

            content.append("Applied Force: " + str(calculation.force) + " N")
            content.append("Normal Stress: " + str(round(calculation.stress, 2)) + " MPa")
            content.append("Factor of Safety: " + str(round(calculation.factor_of_safety, 2)))
            content.append(calculation.assessment)

            content.append(Button("View Details", "calculation_details", [Argument("calculation_index", index)]))
            content.append("--------------------")
    content.append(Button("Back Home", "index"))
    content.append(Button("Calculate Again", "calculator"))
    content.append(Button("Clear History", "clear_history"))

    return Page(state, content)
@route
def calculation_details(state: State, calculation_index: int) -> Page:
    calculation = state.calculations[calculation_index]

    return Page(state, [
        "Calculation Details",
        "\n",
        "Applied Force: " + str(calculation.force) + " N",
        "\n",
        "Cross-Sectional Area: " + str(calculation.area) + " mm^2",
        "\n",
        "Yield Strength: " + str(calculation.yield_strength) + " MPa",
        "\n",
        "Normal Stress: " + str(round(calculation.stress, 2)) + " MPa",
        "\n",
        "Factor of Safety: " + str(round(calculation.factor_of_safety, 2)),
        "\n",
        "Target Factor of Safety: " + str(calculation.target_fos),
        "\n",
        calculation.assessment,
        "\n",
        Button("Back to History", "history"),
        Button("Home", "index")
    ])
@route
def clear_history(state: State) -> Page:
    state.calculations = []

    return Page(state, [
        "Your calculation history has been cleared!",
        "\n",
        Button("Back to History", "history"),
        Button("Home", "index")
    ])
@route
def about(state: State) -> Page:
    return Page(state, [
        "About This Calculator",
        "\n",
        "This website is designed to calculate normal stress and factor of safety for engineering materials.",
        "\n",
        "Users can enter an applied force, cross-sectional area, yield strength, and target factor of safety.",
        "\n",
        "The calculator uses these values to determine the normal stress and factor of safety.",
        "\n",
        "Users can also save, view, and clear their previous calculations.",
        "\n",
        Button("Back Home", "index"),
        Button("Open Calculator", "calculator")
    ])
start_server(State("", "", "", "", []))
