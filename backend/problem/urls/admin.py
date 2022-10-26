from django.conf.urls import url

from ..views.admin import (ContestProblemAPI, ProblemAPI, TestCaseAPI, MakeContestProblemPublicAPIView,
                           CompileSPJAPI, AddContestProblemAPI, ExportProblemAPI, ImportProblemAPI,
                           FPSProblemImport, ProblemCategoryListAPI, ProblemCategoryAPI, SearchProblemAPI, 
                           AddProblemAPI, DeleteProblemCategoryAPI, CategoryProblemListAPI, ModifyProblemCategoryAPI,
                           GetProblemTagAPI, AddProblemTagAPI, CreateProblemTagAPI, ModifyProblemTagAPI,
                           DeleteProblemTagAPI)

urlpatterns = [
    url(r"^test_case/?$", TestCaseAPI.as_view(), name="test_case_api"),
    url(r"^compile_spj/?$", CompileSPJAPI.as_view(), name="compile_spj"),
    url(r"^problem/?$", ProblemAPI.as_view(), name="problem_admin_api"),
    url(r"^contest/problem/?$", ContestProblemAPI.as_view(), name="contest_problem_admin_api"),
    url(r"^contest_problem/make_public/?$", MakeContestProblemPublicAPIView.as_view(), name="make_public_api"),
    url(r"^contest/add_problem_from_public/?$", AddContestProblemAPI.as_view(), name="add_contest_problem_from_public_api"),
    url(r"^export_problem/?$", ExportProblemAPI.as_view(), name="export_problem_api"),
    url(r"^import_problem/?$", ImportProblemAPI.as_view(), name="import_problem_api"),
    url(r"^import_fps/?$", FPSProblemImport.as_view(), name="fps_problem_api"),
    url(r"^problem/categories/?$", ProblemCategoryListAPI.as_view(), name="categories"),
    url(r"^problem/category/?$", ProblemCategoryAPI.as_view(), name="category"),
    url(r"^problem/category/search?$", SearchProblemAPI.as_view(), name="search_problem"),
    url(r"^problem/category/add?$", AddProblemAPI.as_view(), name="add_problem"),
    url(r"^problem/categories/delete?$", DeleteProblemCategoryAPI.as_view(), name="delete_category"),
    url(r"^problem/category/problems?$", CategoryProblemListAPI.as_view(), name="category_problem_list"),
    url(r"^problem/category/modify?$", ModifyProblemCategoryAPI.as_view(), name="modify_category"),
    url(r"^problem/tag?$", GetProblemTagAPI.as_view(), name="tag"),
    url(r"^problem/tag/add?$", AddProblemTagAPI.as_view(), name="add_tag"),
    url(r"^problem/tag/create?$", CreateProblemTagAPI.as_view(), name="create_tag"),
    url(r"^problem/tag/modify?$", ModifyProblemTagAPI.as_view(), name="modify_tag"),
    url(r"^problem/tag/delete?$", DeleteProblemTagAPI.as_view(), name="delete_tag"),
]