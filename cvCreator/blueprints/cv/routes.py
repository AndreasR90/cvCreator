import json

import py_html.core as html
import py_latex.core as latex
from flask import Blueprint, Response, redirect, render_template, request, url_for
from pdflatex import PDFLaTeX

blueprint = Blueprint("blueprint", __name__)
from . import models

docuemntclass = models.DocumentClass()
config = models.Config()
personal_settings = models.PersonalSettings()
cvtitle = models.CvTitle()
# documentclass = core.latexCommand(
#    command="documentclass",
#    args={"docclass": "moderncv"},
#    opt_args={"args": "10pt,a4paper,sans"},
# )
packages = models.Packages(
    packages=[
        latex.usepackage(package="multicol"),
        latex.usepackage(package="geometry", scale="scale=0.75"),
        latex.usepackage(package="xcolor"),
        latex.usepackage(package="draftwatermark", opt=""),
        latex.latexCommand(
            command="SetWatermarkText", args={"Text": "Design Andreas Rabenstein"}
        ),
        latex.latexCommand(command="SetWatermarkScale", args={"Scale": 0.4}),
        latex.latexCommand(command="SetWatermarkColor", args={"color": "red!30"}),
    ]
)
# document = core.latexEnv(command="document", children=["asdf"])
document = models.Document()
document.add_content(models.section(title="First title"))

page = models.LatexDocument(
    documentclass=docuemntclass,
    config=config,
    packages=packages,
    personalsettings=personal_settings,
    document=document,
    cvtitle=cvtitle,
)


@blueprint.route("/update/<part>", methods=["POST", "GET"])
def updateSetting(part):
    if request.form:
        print("UPDATING ", part)
        getattr(page, part).from_dict(dict(request.form))
        return redirect(request.referrer)


@blueprint.route("/add_multicolumn/<document_element>")
def add_multi_elem(document_element):
    document.content[int(document_element)].add_field()
    return redirect(request.referrer)


@blueprint.route("/add_element/<type>/<position>")
def add_element(type, position):
    document.add_content(type, position=int(position))

    return redirect(request.referrer)


@blueprint.route("/mv_element/<orig_pos>/<new_pos>")
def mv_element(orig_pos, new_pos):
    document.swap_content(int(orig_pos), int(new_pos))
    return redirect(request.referrer)


@blueprint.route("/", methods=["POST", "GET"])
def index():
    if request.form:
        print("AM I EVER HERE?")
        raise ValueError("IM AM HERE")
        document.from_dict(dict(request.form))
    body = page.to_html()

    body += html.div(
        className=" d-flex flex-row-reverse",
        style="justify-content-right; margin-top:10px;",
        children=[
            html.div(
                className="dropdown show",
                children=[
                    html.a(
                        className="btn btn-secondary dropdown-toggle",
                        href="#",
                        children="Download",
                        data_toggle="dropdown",
                        aria_haspopup="true",
                        aria_expanded="false",
                    ),
                    html.div(
                        className="dropdown-menu",
                        children=[
                            html.a(
                                className="dropdown-item",
                                href=url_for("blueprint.download", type="pdf"),
                                children="pdf",
                            ),
                            html.a(
                                className="dropdown-item",
                                href=url_for("blueprint.download", type="json"),
                                children="json",
                            ),
                            html.a(
                                className="dropdown-item",
                                href=url_for("blueprint.download", type="tex"),
                                children="tex",
                            ),
                        ],
                    ),
                ],
            ),
            html.a(
                className="btn btn-secondary",
                style="margin-right:10px;",
                children="Upload",
                href=url_for("blueprint.upload"),
            ),
        ],
    ).__str__()

    lat = (
        page.to_latex().replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    )
    return render_template("main.html", body=body, latex=lat)


@blueprint.route("/download/<type>")
def download(type):
    if type == "pdf":
        main = page.to_latex()
        pdfl = PDFLaTeX.from_binarystring(main.encode("utf-8"), jobname="test")
        ret_file, _, _ = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    elif type == "json":
        ret_file = json.dumps(page.to_dict(), indent=4)
    elif type == "tex":
        ret_file = page.to_latex()
    return Response(
        ret_file,
        mimetype=f"text/{type}",
        headers={"Content-disposition": f"attachment; filename=mcv.{type}"},
    )


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ["json"]


@blueprint.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.referrer)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return redirect(request.referrer)
        if file and allowed_file(file.filename):
            dictionary = json.loads(file.read())
            page.from_dict(dictionary)
            return redirect(url_for("blueprint.index"))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
