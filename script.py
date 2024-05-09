#!/usr/bin/python3

import math, xml.etree.ElementTree as ET

EF_File = "flag-earth-cr4qsh0t.svg"
EF_Size = [1160, 720]
EF_Canvas = [29, 18]
EF_Space = "#000000"
EF_Celestials = {
    "sun": {
        "position": [-14.5, 9.0],
        "radius": (29.0 * 8.0/9.0),
        "area": 1.0,
        "composition": {
            "type": "moving",
            "order": ["cooler", "cool", "hot", "hotter", "hottest"],
            "layer": {
                "cooler": {"position": [(29.0 * 0.0/12.0), 0.0], "color": "#ff9900", "area": 0.15},
                "cool": {"position": [(29.0 * -1.0/12.0), 0.0], "color": "#ffcc00", "area": 0.15},
                "hot": {"position": [(29.0 * -2.0/12.0), 0.0], "color": "#ffff00", "area": 0.15},
                "hotter": {"position": [(29.0 * -3.0/12.0), 0.0], "color": "#ffff99", "area": 0.15},
                "hottest": {"position": [(29.0 * -4.0/12.0), 0.0], "color": "#ffffff", "area": 0.15},
            },
        },
    },
    "earth": {
        "position": [14.5, 9.0],
        "radius": 8.0,
        "area": 509.5,
        "composition": {
            "type": "concentric",
            "order": ["oceanTrench", "oceanFloor", "oceanTrans", "oceanShelf", "landCoast", "landAgri", "landShrub", "landForest", "landRock", "landGlacier"],
            "layer": {
                "oceanTrench": {"area": 6.0, "color": "#001840"},
                "oceanFloor": {"area": 290.0, "color": "#0b3380"},
                "oceanTrans": {"area": 41.0, "color": "#183399"},
                "oceanShelf": {"area": 25.5, "color": "#1899ff"},
                "landCoast": {"area": 17.0, "color": "#efe4b0"},
                "landAgri": {"area": 51.0, "color": "#189933"},
                "landShrub": {"area": 12.0, "color": "#188033"},
                "landForest": {"area": 39.0, "color": "#004018"},
                "landRock": {"area": 13.0, "color": "#c0c0c0"},
                "landGlacier": {"area": 15.0, "color": "#ffffff"},
            },
        },
    },
    "moon": {
        "position": [25.0, 3.6],
        "radius": 2.25,
        "area": 1.0,
        "composition": {
            "type": "concentric",
            "order": ["highland", "maria"],
            "layer": {
                "highland": {"area": 0.83, "color": "#c0c0c0"},
                "maria": {"area": 0.17, "color": "#808080"},
            },
        },
    }
}
def EF_Object(iObject):
    lElements = []
    if iObject["composition"]["type"] == "concentric":
        lPrevArea = 0
        for x in iObject["composition"]["order"]:
            lRadius = math.sqrt(1 - lPrevArea / iObject["area"]) * iObject["radius"]
            lPrevArea += iObject["composition"]["layer"][x]["area"]
            lLayer = ET.Element("circle")
            lLayer.set("cx", str(iObject["position"][0]))
            lLayer.set("cy", str(iObject["position"][1]))
            lLayer.set("r", str(lRadius))
            lLayer.set("fill", str(iObject["composition"]["layer"][x]["color"]))
            lElements.append(lLayer)
    else:
        for x in iObject["composition"]["order"]:
            lLayer = ET.Element("circle")
            lLayer.set("cx", str(iObject["position"][0] + iObject["composition"]["layer"][x]["position"][0]))
            lLayer.set("cy", str(iObject["position"][1] + iObject["composition"]["layer"][x]["position"][1]))
            lLayer.set("r", str(iObject["radius"]))
            lLayer.set("fill", str(iObject["composition"]["layer"][x]["color"]))
            lElements.append(lLayer)
    return lElements

def EF_Main():
    lSVG = ET.Element("svg")
    lSVG.set("width", str(EF_Size[0]))
    lSVG.set("height", str(EF_Size[1]))
    lSVG.set("viewBox", f"0 0 {EF_Canvas[0]} {EF_Canvas[1]}")
    lSVG.set("xmlns", "http://www.w3.org/2000/svg")

    lSpace = ET.Element("rect")
    lSpace.set("width", str(EF_Canvas[0]))
    lSpace.set("height", str(EF_Canvas[1]))
    lSpace.set("fill", EF_Space)
    lSVG.append(lSpace)

    for x in [EF_Object(EF_Celestials[x]) for x in ("sun", "earth", "moon")]:
        for xx in x:
            lSVG.append(xx)

    with open (EF_File, "wb") as lFile:
        ET.ElementTree(lSVG).write(lFile)
        lFile.close()

if __name__ == "__main__":
    EF_Main()
