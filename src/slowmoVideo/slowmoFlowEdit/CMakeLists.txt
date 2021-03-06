
include_directories(${slowmoVideo_SOURCE_DIR})

set(SRCS
    main.cpp
    mainwindow.cpp
    flowEditCanvas.cpp
    shortcutListDialog.cpp
)

set(SRCS_UI
    mainwindow.ui
    flowEditCanvas.ui
    shortcutListDialog.ui
)


set(SRCS_MOC
    mainwindow.h
    flowEditCanvas.h
    shortcutListDialog.h
)

qt4_wrap_ui(UI_H_OUT ${SRCS_UI})
qt4_wrap_cpp(MOC_OUT ${SRCS_MOC})

if(APPLE)
        set(BUNDLE "slowmoFlowEdit")
        set(ICONS_DIR "${${PROJECT_NAME}_SOURCE_DIR}/slowmoVideo/slowmoUI/res")
        message( "OS X build" )
        set(MACOSX_BUNDLE_INFO_STRING "${BUNDLE} ${PROJECT_VERSION}")
        set(MACOSX_BUNDLE_BUNDLE_VERSION "${BUNDLE} ${PROJECT_VERSION}")
        set(MACOSX_BUNDLE_LONG_VERSION_STRING "${BUNDLE} ${PROJECT_VERSION}")
        set(MACOSX_BUNDLE_SHORT_VERSION_STRING "${PROJECT_VERSION}")
        set(MACOSX_BUNDLE_COPYRIGHT "${PROJECT_COPYRIGHT_YEAR} ${PROJECT_VENDOR}")
        set(MACOSX_BUNDLE_ICON_FILE "slowmoUI.icns")
        set(MACOSX_BUNDLE_GUI_IDENTIFIER "${PROJECT_DOMAIN_SECOND}.${PROJECT_DOMAIN_FIRST}")
        set(MACOSX_BUNDLE_BUNDLE_NAME "${BUNDLE}")

        set(MACOSX_BUNDLE_RESOURCES "${CMAKE_CURRENT_BINARY_DIR}/${BUNDLE}.app/Contents/Resources")
        set(MACOSX_BUNDLE_ICON "${ICONS_DIR}/${MACOSX_BUNDLE_ICON_FILE}")
        SET_SOURCE_FILES_PROPERTIES(
           ${MACOSX_BUNDLE_ICON}
            PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
        message(STATUS "Bundle will be : ${MACOSX_BUNDLE} =>  ${PROJECT_NAME} ")

        set( SRCS ${SRCS} ${MACOSX_BUNDLE_ICON} )

endif()

include_directories(..)
include_directories(${CMAKE_BINARY_DIR}/slowmoVideo/slowmoFlowEdit)
include_directories(${CMAKE_BINARY_DIR}/slowmoVideo/libgui)

add_executable(slowmoFlowEdit WIN32 MACOSX_BUNDLE ${SRCS} ${MOC_OUT} ${UI_H_OUT})
target_link_libraries(slowmoFlowEdit sVgui sVflow sVvis ${EXTERNAL_LIBS})

install(TARGETS slowmoFlowEdit
        BUNDLE DESTINATION . COMPONENT Runtime
        RUNTIME DESTINATION ${DEST} COMPONENT Runtime)

if (APPLE)
        #install(TARGETS slowmoUI DESTINATION ".")
       include(DeployQt4)
       install_qt4_executable(slowmoUI.app "" ""  )

else()
        install(TARGETS slowmoFlowEdit DESTINATION ${DEST})
endif()

