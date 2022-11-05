import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
from tkinter import *
from tkinter import filedialog

label_file_explorer = object

def inputFile():
    # Asks user to select the source file to be converted. Supports .md and .txt (at least.)
    global input_filename
    input_filename = filedialog.askopenfilename(
        initialdir= "C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\content\\",
        filetypes= (
            ("All files", "*.*"),
            ("Markdown files","*.md"),
            ("Text files", "*.txt")
        )
    )
    label_file_explorer.configure(text="File Opened: "+input_filename)

def newBlog():
    with open(input_filename, 'r') as file:
        parsed_md = markdown(file.read(), extras=['metadata','fenced-code-blocks', 'strike', 'footnotes'], footnote_title="Jump back to footnote %d in the text.", footnote_return_symbol="&#8617;")

        env = Environment(loader=PackageLoader('package', 'templates'))
        blog_template = env.get_template('blog-template.html')

        data = {
            'content': parsed_md,
            'title': parsed_md.metadata['title'],
            'date': parsed_md.metadata['date'],
            'tags': parsed_md.metadata['tags'],
            # 'thumbnail': parsed_md.metadata['thumbnail'],
            'summary': parsed_md.metadata['summary'],
            'slug': parsed_md.metadata['slug'],
        }

    blog_html_content = blog_template.render(post=data)
    blog_filepath = 'C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\posts\\' + parsed_md.metadata['slug'] + '.html'


    # os.makedirs(os.path.dirname(blog_filepath), exist_ok=True)
    with open(blog_filepath, 'w') as file:
        file.write(blog_html_content)
    
    label_file_explorer.configure(text="Blog Rendered")

def indexUpdate():
    BLOG = {}

    label_file_explorer.configure(text="Updating index...")

    for blog_md in os.listdir('C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\content\\'):
        file_path = os.path.join('C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\content\\', blog_md)

        with open(file_path, 'r') as file:
            BLOG[blog_md] = markdown(file.read(),extras=['metadata', 'fenced-code-blocks', 'strike', 'footnotes'], footnote_title="Jump back to footnote %d in the text.", footnote_return_symbol="&#8617;")


    BLOG = {
        post: BLOG[post] for post in sorted(
            BLOG, key=lambda post: datetime.strptime(
                BLOG[post].metadata['date'], '%Y-%m-%d'),
                reverse=True
        )
    }

    env = Environment(loader=PackageLoader('package', 'templates'))
    all_posts_template = env.get_template('all-posts-template.html')
    recent_posts_template = env.get_template('recent-posts-template.html')

    index_blog_metadata = [
        BLOG[post].metadata for post in BLOG
    ]

    all_posts_html = all_posts_template.render(posts=index_blog_metadata)

    recents = []
    blogsize = len(index_blog_metadata) 

    if blogsize < 5:
        r = blogsize
    else:
        r = 5

    i=0
    while i < r:
        recents.append(index_blog_metadata[i])
        i = i + 1
    
    recent_posts_html = recent_posts_template.render(posts=recents)


    with open('C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\all.html', 'w') as file:
        file.write(all_posts_html)
    with open('C:\\Users\\Abheshek Pandey\\Documents\\abhe-dot-in\\blog\\index.html', 'w') as file:
        file.write(recent_posts_html)

    label_file_explorer.configure(text="Index Updated")

window = Tk()
window.title('Monochrome SSG v-01')
window.geometry("500x200")
window.config(background = "white")

label_file_explorer = Label(window,
							text = "Please Select the Input file",
                            width= 60,
							fg = "black",
                            bg="white")

button_inputFile = Button(window,
                            text = "Input File",
                            command = inputFile)

button_newBlog = Button(window,
                            text = "Render Blog",
                            command = newBlog)
                        
button_indexUpdate = Button(window,
                            text = "Update Index",
                            command = indexUpdate)

button_exit = Button(window,
                            text = "Exit",
                            command = exit)

label_file_explorer.grid(column = 1, row = 1)
button_inputFile.grid(column = 1, row = 2)
button_newBlog.grid(column = 1, row = 3)
button_indexUpdate.grid(column = 1, row = 4)
button_exit.grid(column = 1, row = 5)

window.mainloop()
