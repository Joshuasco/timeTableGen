// {% for class in classes %} {% if class.0 == days and class.3.name == room.name %} {% for key,time in times.items %} {% if time == class.1 %}
//                     <td class="courses">{{class.2.course.code}} </td>
//                     {% else %}
//                     <td class="courses"></td>
//                     {%endif%} {%endfor%} {%endif%} {% endfor %}