#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject* ocr_engine = NULL;

static PyObject* initialize_ocr(void) {
    PyObject* ocr_module = PyImport_ImportModule("flutter_onnx_ffi.ocr");
    if (!ocr_module) {
        return NULL;
    }

    PyObject* engine_class = PyObject_GetAttrString(ocr_module, "OCREngine");
    Py_DECREF(ocr_module);
    if (!engine_class) {
        return NULL;
    }

    PyObject* engine_instance = PyObject_CallObject(engine_class, NULL);
    Py_DECREF(engine_class);
    return engine_instance;
}

static PyObject* process_image(PyObject* self, PyObject* args) {
    const char* image_path;
    float confidence;

    if (!PyArg_ParseTuple(args, "sf", &image_path, &confidence)) {
        return NULL;
    }

    if (!ocr_engine) {
        ocr_engine = initialize_ocr();
        if (!ocr_engine) {
            return NULL;
        }
    }

    PyObject* result = PyObject_CallMethod(ocr_engine, "process_image", "sf", image_path, confidence);
    return result;
}

static PyMethodDef BridgeMethods[] = {
    {"process_image", process_image, METH_VARARGS, "Process an image with OCR"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef bridge_module = {
    PyModuleDef_HEAD_INIT,
    "ocr_bridge",
    NULL,
    -1,
    BridgeMethods
};

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_ocr_bridge(void) {
    return PyModule_Create2(&bridge_module, PYTHON_API_VERSION);
}
#else
PyMODINIT_FUNC initocr_bridge(void) {
    PyModule_Create2(&bridge_module, PYTHON_API_VERSION);
}
#endif