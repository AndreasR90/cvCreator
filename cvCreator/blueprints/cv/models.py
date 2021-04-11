import copy
import math

from flask import url_for
from py_html import core as html
from py_latex import core as latex

from .routes import blueprint


def generate_html_input(key, value):
    if isinstance(value, (list, dict)):
        return [
            html.input(type="text", className="", value=val, name=key + str(cnt),)
            for cnt, val in enumerate(value)
        ]
    else:
        return [html.input(type="text", className="", value=value, name=key,)]


def dict_to_html(dictionary, action):
    html_string = html.form(
        method="POST",
        action=action,
        children=[
            html.div(
                className="form-group row",
                children=[
                    html.div(className="col-sm-1"),
                    html.label(className="col-sm-2 col-form-label", children=[key]),
                    html.div(
                        className="col-sm-6", children=generate_html_input(key, value),
                    ),
                ],
            )
            for key, value in dictionary.items()
        ]
        + [
            html.div(
                className=" d-flex flex-row-reverse",
                style="justify-content-right; margin-top:10px;",
                children=[
                    html.button(
                        type="submit", className="btn btn-secondary", children="Save"
                    ),
                ],
            )
        ],
    )
    return html_string


class DocumentClass:
    def __init__(self, fontsize="10pt", papersize="a4paper", font="sans"):
        self.fontsize = fontsize
        self.papersize = papersize
        self.font = font

    def to_latex(self):
        return latex.latexCommand(
            command="documentclass",
            args={"docclass": "moderncv"},
            opt_args={"args": ",".join([self.fontsize, self.papersize, self.font])},
        ).to_latex()

    def __str__(self):
        return self.to_latex()

    def to_dict(self):
        return {
            "fontsize": self.fontsize,
            "papersize": self.papersize,
            "font": self.font,
        }

    def from_dict(self, dictionary_in):
        dictionary = {}
        for key, value in dictionary_in.items():
            if value != "None":
                dictionary[key] = value
        self.fontsize = dictionary.get("fontsize", self.fontsize)
        self.papersize = dictionary.get("papersize", self.papersize)
        self.font = dictionary.get("font", self.font)

    def to_html(self):
        return dict_to_html(
            self.to_dict(),
            action=url_for("blueprint.updateSetting", part="documentclass"),
        )


class Config:
    def __init__(
        self,
        color0="#000000",
        color1="#000000",
        color2="#606060",
        color3="#ffffff",
        pictureEachPage=False,
        moderncvstyle="casual",
    ):
        self.color0 = color0
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.pictureEachPage = pictureEachPage
        self.moderncvstyle = moderncvstyle

    def to_dict(self):
        return {
            "color0": self.color0,
            "color1": self.color1,
            "color2": self.color2,
            "color3": self.color3,
            "pictureEachPage": self.pictureEachPage,
            "moderncvstyle": self.moderncvstyle,
        }

    def from_dict(self, dictionary_in):
        dictionary = {}
        for key, value in dictionary_in.items():
            if value != "None":
                dictionary[key] = value
        self.color0 = dictionary.get("color0", self.color0)
        self.color1 = dictionary.get("color1", self.color1)
        self.color2 = dictionary.get("color2", self.color2)
        self.color3 = dictionary.get("color3", self.color3)
        self.pictureEachPage = dictionary.get("pictureEachPage", self.pictureEachPage)
        self.moderncvstyle = dictionary.get("moderncvstyle", self.moderncvstyle)

    def to_latex(self):
        latex_object = latex.latexContainer(
            children=[
                latex.latexCommand(
                    command="definecolor",
                    args={"name": "color0", "type": "HTML", "value": self.color0[1:]},
                ),
                latex.latexCommand(
                    command="definecolor",
                    args={"name": "color1", "type": "HTML", "value": self.color1[1:]},
                ),
                latex.latexCommand(
                    command="definecolor",
                    args={"name": "color2", "type": "HTML", "value": self.color2[1:]},
                ),
                latex.latexCommand(
                    command="definecolor",
                    args={"name": "color3", "type": "HTML", "value": self.color3[1:]},
                ),
                latex.latexCommand(
                    command="moderncvstyle", args={"style": self.moderncvstyle}
                ),
            ]
        )
        return latex_object.to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self):
        return dict_to_html(
            self.to_dict(), action=url_for("blueprint.updateSetting", part="config"),
        )


class PersonalSettings:
    def __init__(
        self,
        firstname=None,
        familyname=None,
        title=None,
        address={"Street": None, "City": None},
        mobile=None,
        email=None,
        photo=None,
        photo_opt_args={"height": "50pt", "frame": "0pt"},
        DateOfBirth=None,
        PlaceOfBirth=None,
    ):
        self.firstname = firstname
        self.familyname = familyname
        self.title = title
        if not isinstance(address, (list, dict)):
            self.address = {"address": address}
        else:
            self.address = address
        self.mobile = mobile
        self.email = email
        self.photo = photo
        self.photo_opt_args = photo_opt_args
        self.DateOfBirth = DateOfBirth
        self.PlaceOfBirth = PlaceOfBirth

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "familyname": self.familyname,
            "title": self.title,
            "address": list(self.address.values()),
            "mobile": self.mobile,
            "email": self.email,
            "photo": self.photo,
            "photo_opt_args": list(self.photo_opt_args.values()),
            "DateOfBirth": self.DateOfBirth,
            "PlaceOfBirth": self.PlaceOfBirth,
        }

    def from_dict(self, dictionary_in):
        dictionary = {}
        for key, val in dictionary_in.items():
            if val != "None":
                dictionary[key] = val
        self.firstname = dictionary.get("firstname", self.firstname)
        self.familyname = dictionary.get("familyname", self.familyname)
        self.title = dictionary.get("title", self.title)
        self.address = {
            key: dictionary.get("address" + str(cnt), val)
            for cnt, (key, val) in enumerate(self.address.items())
        }
        self.mobile = dictionary.get("mobile", self.mobile)
        self.email = dictionary.get("email", self.email)
        self.photo = dictionary.get("photo", self.photo)
        self.photo_opt_args = {
            key: dictionary.get("photo_opt_args" + str(cnt), val)
            for cnt, (key, val) in enumerate(self.photo_opt_args.items())
        }
        self.DateOfBirth = dictionary.get("DateOfBirth", self.DateOfBirth)
        self.PlaceOfBirth = dictionary.get("PlaceOfBirth", self.PlaceOfBirth)

    def to_latex(self):
        return latex.latexContainer(
            children=[
                latex.latexCommand(
                    command="firstname", args={"firstname": self.firstname}
                ),
                latex.latexCommand(
                    command="familyname", args={"familyname": self.familyname}
                ),
                latex.latexCommand(command="title", args={"title": self.title}),
                latex.latexCommand(command="address", args=self.address),
                latex.latexCommand(command="mobile", args={"mobile": self.mobile}),
                latex.latexCommand(command="email", args={"email": self.email}),
                latex.latexCommand(command="photo", opt_args=self.photo_opt_args),
            ]
        ).__str__()

    def __str__(self):
        return self.to_latex()

    def to_html(self):
        return dict_to_html(
            self.to_dict(),
            action=url_for("blueprint.updateSetting", part="personalsettings"),
        )


class multicolum:
    def __init__(self, children=None, nCols=3):
        if children is None:
            self.children = []
        else:
            self.children = children
        self.nCols = nCols
        self.type = "multicols"

    def from_dict(self, dictionary):
        self.nCols = int(dictionary.get("nCols", self.nCols))
        for i in range(len(self.children)):
            self.children[i] = dictionary.get(str(i), self.children[i])

    def add_field(self):
        self.children += [""]

    def to_latex(self):
        children = [
            latex.latexCommand(
                command="cvitem", args={"item": "", "description": child}
            )
            for child in self.children
        ]
        return latex.latexEnv(
            command="multicols", args={"nRows": self.nCols}, children=children
        ).__str__()

    def __str__(self):
        return self.to_latex()

    def to_html(self, name):
        html_string = ""
        # nCols
        children = [
            html.div(className="col-sm-1"),
            html.label(className="col-sm-1", children="nCols"),
            html.div(
                className="col-sm-1",
                children=[
                    html.input(
                        type="text",
                        value=self.nCols,
                        name=name + "-nCols",
                        className="form-control",
                    ),
                ],
            ),
        ]
        html_string += html.div(className="row", children=children).__str__()

        length = len(self.children)
        row_step = math.ceil(length / self.nCols)

        for row in range(row_step):
            child = [html.div(className="col-sm-1")]
            for col in range(self.nCols):
                coln = row + col * row_step
                if coln >= length:
                    break
                child += [
                    html.div(
                        className="col-sm-2",
                        children=[
                            html.input(
                                type="text",
                                value=self.children[coln],
                                name=name + "-" + str(coln),
                                className="form-control",
                            ),
                        ],
                    )
                ]

            html_string += html.div(
                className="form-row", style="margin-top:10px;", children=child
            ).__str__()
        # Add button for adding of fields
        html_string += html.div(
            className="row",
            style="margin-top:10px;",
            children=[
                html.div(className=f"col-sm-{2*self.nCols}"),
                html.div(
                    className="col-sm-4",
                    children=[
                        html.a(
                            className="btn btn-secondary",
                            type="button",
                            children="Add field",
                            style="margin-right:10px;",
                            href=url_for(
                                "blueprint.add_multi_elem", document_element=name
                            ),  # f"/add_multicolumn/{name}",
                        ),
                    ],
                ),
            ],
        ).__str__()
        return html_string


class section:
    def __init__(self, title=None):
        self.title = title
        self.type = "section"

    def to_dict(self):
        return {"title": self.title}

    def from_dict(self, dictionary):
        self.title = dictionary.get("title", self.title)

    def to_latex(self):
        return latex.section(self.title).to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self, name):
        return html.div(
            className="form-row",
            children=[
                html.div(className="col-sm-1"),
                html.div(
                    className="col-sm-10",
                    children=[
                        html.input(
                            type="text",
                            placeholder="title",
                            value=self.title if self.title is not None else "",
                            name=name + "-title",
                            className="form-control",
                        ),
                    ],
                ),
            ],
        )


class cvEntry:
    def __init__(
        self,
        year=None,
        job_title=None,
        institution=None,
        city=None,
        grade=None,
        description=None,
    ):
        self.year = year
        self.job_title = job_title
        self.institution = institution
        self.city = city
        self.grade = grade
        self.description = description

        self.type = "cvEntry"

    def to_dict(self):
        return {
            "year": self.year,
            "job_title": self.job_title,
            "institution": self.institution,
            "city": self.city,
            "grade": self.grade,
            "description": self.description,
        }

    def from_dict(self, dictionary):
        self.year = dictionary.get("year", self.year)
        self.job_title = dictionary.get("job_title", self.job_title)
        self.institution = dictionary.get("institution", self.institution)
        self.city = dictionary.get("city", self.city)
        self.grade = dictionary.get("grade", self.grade)
        self.description = dictionary.get("description", self.description)

    def to_latex(self):
        return latex.cventry(
            self.year,
            self.job_title,
            self.institution,
            self.city,
            self.grade,
            self.description,
        ).to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self, name):
        html_string = [
            html.div(
                className="col",
                children=[
                    html.input(
                        type="text",
                        value=value if value is not None else key,
                        name=str(name) + "-" + str(key),
                    )
                ],
            )
            for key, value in self.to_dict().items()
        ]
        html_string = html.div(
            className="form-row",
            # style="margin-right:200px;",
            children=[
                html.div(className="col-sm-1"),
                html.div(
                    className="col-sm-2",
                    children=[
                        html.input(
                            type="text",
                            placeholder="year",
                            value=self.year if self.year is not None else "",
                            name=name + "-year",
                            className="form-control",
                        ),
                    ],
                ),
                html.div(
                    className="col-sm-2",
                    children=[
                        html.input(
                            type="text",
                            placeholder="job_title",
                            value=self.job_title if self.job_title is not None else "",
                            name=name + "-job_title",
                            className="form-control",
                        ),
                    ],
                ),
                html.div(
                    className="col-sm-2",
                    children=[
                        html.input(
                            type="text",
                            placeholder="institution",
                            value=self.institution
                            if self.institution is not None
                            else "",
                            name=name + "-institution",
                            className="form-control",
                        ),
                    ],
                ),
                html.div(
                    className="col-sm-2",
                    children=[
                        html.input(
                            type="text",
                            placeholder="city",
                            value=self.city if self.city is not None else "",
                            name=name + "-city",
                            className="form-control",
                        ),
                    ],
                ),
                html.div(
                    className="col-sm-2",
                    children=[
                        html.input(
                            type="text",
                            placeholder="grade",
                            value=self.grade if self.grade is not None else "",
                            name=name + "-grade",
                            className="form-control",
                        ),
                    ],
                ),
            ],
        ).__str__()
        html_string += html.div(
            className="form-row",
            style="margin-top:20px;",
            # style="margin-right:200px;",
            children=[
                html.div(className="col-sm-1"),
                html.div(
                    className="col-sm-10",
                    children=[
                        html.textarea(
                            type="text",
                            placeholder="description",
                            value=self.description
                            if self.description is not None
                            else "",
                            name=name + "-description",
                            className="form-control",
                            children=[
                                self.description
                                if self.description not in [None, [""]]
                                else ""
                            ],
                        ),
                    ],
                ),
            ],
        ).__str__()
        return html_string


class Document(latex.latexEnv):
    def __init__(self):
        super().__init__(command="document", children=None)
        self.content = []
        self.possible_adds = {
            "section": section,
            "cvEntry": cvEntry,
            "multicolumn": multicolum,
        }

    def add_content(self, element, position=None):
        if isinstance(element, str):
            element = self.possible_adds.get(element, None)
            if element is None:
                raise ValueError("Cannot add " + element)
            element = element.__call__()
        if position is None:
            position = len(self.content)
        self.content.insert(position, element)

    def swap_content(self, orig_pos, new_pos):
        if orig_pos < 0 or orig_pos >= len(self.content):
            return
        if new_pos < 0 or new_pos >= len(self.content):
            return
        tmp = self.content[orig_pos]
        self.content[orig_pos] = self.content[new_pos]
        self.content[new_pos] = tmp

    def to_dict(self):
        ret_dict = {"content": [cont.type for cont in self.content]}
        for idx, cont in enumerate(self.content):
            cont_dict = cont.to_dict()
            for key, val in cont_dict.items():
                nkey = str(idx) + "-" + key
                ret_dict[nkey] = val
        return ret_dict

    def from_dict(self, dictionary):
        if "content" in dictionary:
            self.content = []
            self.content = [
                self.possible_adds[cont].__call__() for cont in dictionary["content"]
            ]
        print(self.content)
        print(dictionary)
        for key, value in dictionary.items():
            if key == "content":
                continue
            idx = int(key.split("-")[0])
            sub_val = "".join(key.split("-")[1:])
            print({sub_val: value})
            self.content[idx].from_dict(dictionary={sub_val: value})

    def html_dropdown_add(self, cnt, above=True):
        difference = 0 if above else 1
        html_string = html.div(
            className="dropdown",
            children=[
                html.button(
                    className="btn btn-secondary dropdown-toggle btn-sm",
                    type="button",
                    data_toggle="dropdown",
                    aria_haspopup="true",
                    aria_expanded="false",
                    style="margin-right:10px",
                    children="Add " + ("above" if above else "below"),
                ),
                html.div(
                    className="dropdown-menu",
                    children=[
                        html.a(
                            children=[possibility],
                            className="dropdown-item",
                            href=url_for(
                                "blueprint.add_element",
                                type=possibility,
                                position=cnt + 1,
                            ),
                        )
                        for possibility in self.possible_adds.keys()
                    ],
                ),
            ],
        )
        return html_string

    def html_move_content(self, name, start, dest):
        if dest < 0 or dest >= len(self.content):
            return ""
        return html.a(
            className="btn btn-secondary btn-sm",
            type="button",
            children=name,
            style="margin-right:10px;",
            href=url_for("blueprint.mv_element", orig_pos=start, new_pos=dest),
        )

    def block_title(self, type):
        return html.div(
            style="width: 100%; height: 20px; border-bottom: 1px solid black;text-align: left; margin-bottom:10px;",
            children=[
                html.span(
                    style="padding:2px 10px;background-color:gray;margin-left:20px",
                    children=[html.strong(type)],
                )
            ],
        )

    def add_control_row(self, cnt):
        return html.div(
            className=" d-flex flex-row-reverse",
            style="justify-content-right; margin-top:10px;",
            children=[
                self.html_move_content(name="up", start=cnt, dest=cnt - 1),
                self.html_move_content(name="down", start=cnt, dest=cnt + 1),
                self.html_dropdown_add(cnt, above=True),
                self.html_dropdown_add(cnt, above=False),
            ],
        )

    def submit(self):
        return html.div(
            className=" d-flex flex-row-reverse",
            style="justify-content-right; margin-top:10px;",
            children=[
                html.button(
                    type="submit", className="btn btn-secondary", children="Save"
                )
            ],
        )

    def to_latex(self):
        return latex.document(children=self.content).to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self):
        children = []
        for cnt, cont in enumerate(self.content):
            children += [
                self.block_title(cont.type),
                cont.to_html(name=str(cnt)),
                self.add_control_row(cnt),
            ]
        # html_string += html.form(
        #    method="POST",
        #    children=[
        #        self.block_title(cont.type),
        #        cont.to_html(name=str(cnt)),
        #        self.add_control_row(cnt),
        #    ],
        # ).__str__()
        children += [self.submit()]

        return html.form(
            method="POST",
            action=url_for("blueprint.updateSetting", part="document"),
            children=children,
        )


class Packages:
    def __init__(self, packages=None):
        if packages is None:
            self.packages = []
        else:
            self.packages = packages

    def to_dict(self):
        return {cnt: package.__str__() for cnt, package in enumerate(self.packages)}

    def from_dict(self, dictionary_in):
        dictionary = {}
        for key, value in dictionary_in.items():
            if value != "None":
                dictionary[key] = value
        self.packages = [pack for pack in dictionary.values()]

    def to_latex(self):
        return latex.latexContainer(
            children=[pack for pack in self.packages]
        ).to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self):
        return dict_to_html(
            self.to_dict(), action=url_for("blueprint.updateSetting", part="packages"),
        )


class CvTitle:
    def __init__(self, title="Lebenslauf", type="Standard") -> None:
        self.title = title
        self.type = type
        self.config = None
        self.personalsettings = None

    def initialize(self, config, personalsettings):
        self.config = config
        self.personalsettings = personalsettings

    def to_dict(self):
        return {"title": self.title, "type": self.type}

    def from_dict(self, dictionary_in):
        dictionary = {}
        for key, value in dictionary_in.items():
            if value != "None":
                dictionary[key] = value
        self.title = dictionary.get("title", self.title)
        self.type = dictionary.get("type", self.type)

    def standard_header(self):
        latexObject = latex.latexContainer()
        if self.personalsettings.photo is not None:
            latexObject.children += [
                latex.latexCommand(
                    command="includegraphics",
                    args={"picture": self.personalsettings.photo},
                    opt_args={"width": "8em"},
                )
            ]

        latexObject.children += [
            f"""
            \\hfill
            \\begin{{minipage}}[b]{{12.5cm}}
            \\raggedright
            {{ \\hfill%
                \\fontsize{{52}}{{40}}\\selectfont \\textcolor{{color2}}{{
                    {self.title}%
                }}%
            }}\\\\[1.5em]%
            {{%
            \\hfill%
                \\fontsize{{43}}{{40}}\\selectfont \\textcolor{{color2!60}}{{{self.personalsettings.firstname}}} \\textcolor{{color2}}{{{self.personalsettings.familyname}}}%
            }}%
            \\end{{minipage}}\\newline%
            \\textcolor{{black!30}}{{\\rule[.5\\baselineskip]{{\\textwidth}}{{1pt}}}}\\\\[-3em]%
            \\begin{{flushright}}%
                \\fontsize{{15}}{{20}}\\selectfont%
                \\textit{{%
                    \\textcolor{{color2}}{{{self.personalsettings.DateOfBirth}~in~{self.personalsettings.PlaceOfBirth}\\hfill {self.personalsettings.title}}}%
                }}%
            \\end{{flushright}}%
            \\makecvfoot
        """,
        ]
        return latexObject

    def to_latex(self):
        if self.config is None or self.personalsettings is None:
            raise ValueError("Header is not initialized")
        if self.type == "Standard":
            latexObject = self.standard_header()
        return latexObject.to_latex()

    def __str__(self):
        return self.to_latex()

    def to_html(self):
        return dict_to_html(
            self.to_dict(), action=url_for("blueprint.updateSetting", part="cvtitle"),
        )


class LatexDocument:
    def __init__(
        self,
        documentclass: DocumentClass(),
        config: Config = Config(),
        packages: Packages = Packages(),
        personalsettings: PersonalSettings = PersonalSettings(),
        document: Document = Document(),
        cvtitle: CvTitle = CvTitle(),
    ):
        self.documentclass = documentclass
        self.config = config
        self.packages = packages
        self.personalsettings = personalsettings
        self.document = document
        self.cvtitle = cvtitle

    def to_dict(self):
        ret_dict = {}
        for name, type in zip(
            [
                "documentclass",
                "packages",
                "config",
                "personalsettings",
                "document",
                "cvtitle",
            ],
            [
                self.documentclass,
                self.packages,
                self.config,
                self.personalsettings,
                self.document,
                self.cvtitle,
            ],
        ):
            ret_dict[name] = type.to_dict()
        return ret_dict

    def from_dict(self, dictionary):
        for key in [
            "documentclass",
            "packages",
            "config",
            "personalsettings",
            "document",
            "cvtitle",
        ]:
            if key in dictionary.keys():
                getattr(self, key).from_dict(dictionary[key])

    def to_latex(self):
        self.cvtitle.initialize(
            config=self.config, personalsettings=self.personalsettings
        )
        documents = copy.copy(self.document)
        documents.content = [self.cvtitle] + documents.content
        return latex.latexContainer(
            children=[
                self.documentclass,
                self.packages,
                self.config,
                self.personalsettings,
                documents,
            ]
        ).to_latex()

    def to_html(self):
        html_string = ""
        for name, obj in zip(
            ["DocumentClass", "Packages", "Config", "PersonalSettings", "Document"],
            [
                self.documentclass,
                self.packages,
                self.config,
                self.personalsettings,
                self.document,
            ],
        ):
            htmlObj = html.div(
                className="card",
                style="margin-bottom:10px;",
                children=[
                    html.div(
                        className="card-header",
                        children=[
                            html.a(
                                className="card-link",
                                data_toggle="collapse",
                                href=f"#{name}",
                                children=name,
                            )
                        ],
                    ),
                    html.div(className="collapse", id=name, children=[obj.to_html()],),
                ],
            )
            html_string += htmlObj.__str__()

        return html_string
