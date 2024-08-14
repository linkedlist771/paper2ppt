

# paper2ppt

## Description

> paper2ppt is an innovative tool that automatically generates PowerPoint presentations from academic papers. By leveraging AI technology, it creates engaging slides that capture the essence of research papers while maintaining a style similar to a given reference presentation.

## Features

- Parse academic papers in various formats (PDF, DOCX, etc.)
- Utilize AI to generate presentation content based on the paper
- Adapt content to match the style of a reference presentation
- Apply custom PowerPoint templates
- Ensure high-quality output through automated checks

## Installation

To install paper2ppt, follow these steps:

```bash
git clone https://github.com/yourusername/paper2ppt.git
cd paper2ppt
pip install -r requirements.txt
```

## Usage

1. Prepare your input files:
   - Academic paper (PDF or DOCX format)
   - Reference presentation (PPTX format)
   - PowerPoint template (PPTX format)

2. Run the tool:

```bash
python -m paper2ppt.main --paper path/to/paper.pdf --reference path/to/reference.pptx --template path/to/template.pptx
```

3. The generated presentation will be saved in the `output` directory.

## Configuration

You can customize the behavior of paper2ppt by modifying the settings in `configs/settings.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to [AI Provider] for their powerful language model that makes this tool possible.
- Inspired by the tedious process of manually creating presentations from research papers.
