cmake_minimum_required(VERSION 3.10)

option(BUILD_DOCS "Build LaTeX documentation" ON)

if(BUILD_DOCS)
    find_program(PDFLATEX_EXECUTABLE pdflatex REQUIRED)
    find_program(BIBTEX_EXECUTABLE bibtex REQUIRED)

    file(GLOB TEX_FILES CONFIGURE_DEPENDS "*.tex")
    set(GENERATED_EXTS aux bbl blg log out toc lof lot snm nav vrb)

    foreach(TEX_FILE ${TEX_FILES})
        get_filename_component(BASENAME ${TEX_FILE} NAME_WE)
        set(PDF_FILE ${BASENAME}.pdf)

        # Generate list of temporary files
        set(BUILD_FILES "")
        foreach(EXT ${GENERATED_EXTS})
            list(APPEND BUILD_FILES "${BASENAME}.${EXT}")
        endforeach()

        add_custom_command(
            OUTPUT ${PDF_FILE}
            COMMAND ${PDFLATEX_EXECUTABLE} ${BASENAME}.tex
            COMMAND ${BIBTEX_EXECUTABLE} ${BASENAME} || ${CMAKE_COMMAND} -E echo "No .aux file for bibtex."
            COMMAND ${PDFLATEX_EXECUTABLE} ${BASENAME}.tex
            COMMAND ${PDFLATEX_EXECUTABLE} ${BASENAME}.tex
            COMMAND ${CMAKE_COMMAND} -E echo "Cleaning up..."
            COMMAND ${CMAKE_COMMAND} -E rm -f ${BUILD_FILES}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            DEPENDS ${TEX_FILE}
            BYPRODUCTS ${BUILD_FILES}
            COMMENT "Compiling ${BASENAME}.tex → ${PDF_FILE}"
            VERBATIM
        )

        add_custom_target(${BASENAME}_pdf ALL DEPENDS ${PDF_FILE})
    endforeach()
endif()
