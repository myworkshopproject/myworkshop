import logging
import re
from markdown import Markdown
from markdown.extensions.toc import TocExtension

logger = logging.getLogger(__name__)


def md_convert(source, title=""):
    """This function:
    - converts Markdown source into html (excluding headers of level 1);
    - generates metadata from source header;
    - generates a table of content (excluding headers of level 1);
    - adds a 'title' tag into the source if not present and if a default is provided.

    Thi function returns a tuple:
    - new_source (str)
    - new_title (str)
    - html (str)
    - meta (dict)
    - toc (list)
    """

    try:
        # h1_pattern = re.compile(r"^\s*(#[\s])(.*)$", flags=re.MULTILINE)
        h1_pattern = re.compile(r"^\s*(#[^#])(.*)$", flags=re.MULTILINE)

        # Removes all occurences of level 1 headers:
        cleaned_source = re.sub(h1_pattern, "", source)

        # Let's convert Markdown into HTML:
        md = Markdown(
            output_format="html5",
            extensions=[
                # "abbr",
                "fenced_code",
                "footnotes",
                "tables",
                # "extra",
                # "admonition",
                # "codehilite",
                "meta",
                TocExtension(
                    # title=None,
                    # anchorlink=True,
                    # anchorlink_class="toclink",
                    permalink=True,
                    # permalink_class="headerlink",
                    permalink_class="ml-1 has-text-grey-lighter",
                    # permalink_title="Permanent link",
                    baselevel=2,  # default: 1
                    toc_depth="3-4",
                ),
            ],
        )
        html = md.convert(cleaned_source)
        meta = md.Meta
        toc = md.toc_tokens

        # Search for the first level 1 header in source:
        result = re.search(h1_pattern, source)
        first_header_level_1 = result.group(2).strip() if result else None

        # Search for the first 'title' key in meta:
        first_meta_title = None
        if "title" in md.Meta:
            if md.Meta["title"][0]:
                first_meta_title = md.Meta["title"][0]

        # Should we override title?
        if first_meta_title:
            # There is a non-empty 'title' value in meta:
            new_title = first_meta_title
        else:
            if first_header_level_1:
                # There is a non-empty level 1 header value in source:
                new_title = first_header_level_1
            else:
                # Default title value:
                new_title = title

        # Should we add a 'title:' tag into the source?
        if title and not first_meta_title:
            # A default title value has been submitted
            # and there is no 'title' key in meta:
            new_source = "title: {title}\n{additional_blank_line}{source}".format(
                title=new_title,
                additional_blank_line="\n" if not md.Meta else "",
                source=source,
            )
        else:
            new_source = source

        return (new_source, new_title, html, meta, toc)

    except Exception as e:
        logger.error(e)
        return (source, title, source, {}, "")
