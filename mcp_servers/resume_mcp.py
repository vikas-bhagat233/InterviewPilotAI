from tools.pdf_reader import extract_pdf_text

class ResumeMCP:

    def read_resume(
        self,
        pdf_path
    ):

        return extract_pdf_text(
            pdf_path
        )